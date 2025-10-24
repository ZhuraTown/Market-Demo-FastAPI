from src.api.ws.manager import notification_ws_manager, NotificationConnectionManager


def get_ws_notification_manager()-> NotificationConnectionManager:
    return notification_ws_manager