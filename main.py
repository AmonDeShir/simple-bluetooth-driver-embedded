from bluetooth.bluetooth import Bluetooth
from auth.auth_router import AuthRouter
from logger.logger_router import LoggerRouter


bluetooth = Bluetooth()

auth_router = AuthRouter(bluetooth)
logger_router = LoggerRouter(bluetooth)