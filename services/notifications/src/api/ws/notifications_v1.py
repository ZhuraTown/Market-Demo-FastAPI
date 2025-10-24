import typing

from loguru import logger
import starlette.status as status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.endpoints import WebSocketEndpoint

from src.api.deps.db import get_session
from src.api.deps.ws_manager import get_ws_notification_manager
from src.api.ws.manager import notification_ws_manager, NotificationConnectionManager
from fastapi import WebSocketDisconnect, Depends, APIRouter
from starlette.websockets import WebSocket

from src.db.database import db
from src.domain.notifications import NotificationService, NotificationActionHandler
from src.dto.notification import NotificationActionInput


class NotificationEndpoint(WebSocketEndpoint):
    encoding = "json"

    async def on_connect(self, websocket):
        user_id = int(websocket.query_params.get("user_id"))
        await notification_ws_manager.connect(user_id, websocket)
        websocket.state.user_id = user_id

    async def on_receive(self, websocket: WebSocket, data: dict):
        await notification_ws_manager.send_to_user(websocket.state.user_id, {"echo": data})

    async def on_disconnect(self, websocket: WebSocket, close_code):
        notification_ws_manager.disconnect(websocket.state.user_id)



class WSNotificationsRouteV1:
    encoding: str = "json"

    def __init__(
            self,
            websocket: WebSocket,
            manager: NotificationConnectionManager = Depends(get_ws_notification_manager),
    ):
        self._websocket = websocket
        self.manager = manager

    def __await__(self) -> typing.Generator:
        return self.dispatch().__await__()

    async def dispatch(self) -> None:
        await self._on_connect()

        close_code: int = status.WS_1000_NORMAL_CLOSURE
        try:
            while True:
                data = await self._websocket.receive_json()
                dto = NotificationActionInput.model_validate(data, from_attributes=True)
                await self._on_receive(data)
        except WebSocketDisconnect:
            # Handle client normal disconnect here
            pass
        except Exception as exc:
            logger.error(exc)
            close_code = status.WS_1011_INTERNAL_ERROR
            raise exc from None
        finally:
            await self._on_disconnect(close_code)

    async def _on_connect(self):
        # Handle your new connection here
        await self._websocket.accept()
        user_id = int(self._websocket.query_params.get("user_id"))
        await notification_ws_manager.connect(user_id, self._websocket)
        self._websocket.state.user_id = user_id

    async def _on_disconnect(self, close_code: int):
        # Handle client disconnect here
        notification_ws_manager.disconnect(self._websocket.state.user_id)


    async def _on_receive(self, msg: dict):
        await notification_ws_manager.send_to_user(self._websocket.state.user_id, {"echo": msg})

router = APIRouter(
    prefix="/ws/v1/notifications",
    tags=["notifications"],
)



@router.websocket("")
async def ws_notifications_route_v1(
        websocket: WebSocket,
        user_id: int,
        manager: NotificationConnectionManager = Depends(get_ws_notification_manager),
):
    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await NotificationActionHandler.handle(user_id, websocket, manager, data)
    except WebSocketDisconnect:
        await manager.disconnect(user_id, websocket)
