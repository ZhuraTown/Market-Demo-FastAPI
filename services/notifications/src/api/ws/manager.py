from collections import defaultdict

from starlette.websockets import WebSocket, WebSocketDisconnect
from loguru import logger


# class NotificationConnectionManager:
#     def __init__(self):
#         # todo: change later for Redis
#         self.active_connections: dict[int, set[WebSocket]] = defaultdict(set)
#
#     async def connect(self, user_id: int, websocket: WebSocket):
#         logger.info(f"Connect user({user_id})")
#         self.active_connections[user_id].add(websocket)
#         await self.send_to_user(user_id, {"msg": "Hello World!"})
#
#     def disconnect(self, user_id: int):
#         logger.info(f"Disconnect user({user_id})")
#         # self.active_connections.pop(user_id, None)
#
#     async def send_to_user(self, websocket: WebSocket, message: dict):
#         logger.info(f"Send for user({websocket.state.user_id}), msg: {message}")
#         try:
#             await websocket.send_json(message)
#         except Exception as exc:
#             logger.error(f"Cannot send msg user({websocket.state.user_id})",exc)
#
#     async def broadcast_to_user(self, user_id: int, message: dict):
#         websockets = self.active_connections.get(user_id)
#         for websocket in websockets:
#             await self.send_to_user(websocket, message)
#
# notification_ws_manager = NotificationConnectionManager()


class NotificationConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)
        logger.info(f"Connect user({user_id})")
        await self.send_personal_message({"msg": "Hello World!"}, websocket)

    async def disconnect(self, user_id: int, websocket: WebSocket):
        logger.info(f"Disconnect user({user_id})")
        self.active_connections[user_id].remove(websocket)

    async def send_personal_message(
            self,
            message: dict,
            websocket: WebSocket
    ):
        logger.info(f"Send message({message})")
        await websocket.send_json(message)

    async def broadcast_message(self,user_id: int, message: dict):
        logger.info(f"Send message({message})")
        for connection in self.active_connections.get(user_id, []):
            await self.send_personal_message(message, connection)

notification_ws_manager = NotificationConnectionManager()