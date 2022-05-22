from ..bluetooth.bluetooth import Bluetooth
from auth import Auth
from typing import Callable

class AuthRouter:
    def __init__(self, bluetooth: Bluetooth):
        self.bluetooth = bluetooth
        self.bluetooth.on("log-in", lambda args: self.log_in(args))


    def log_in(self, password: str):
        if Auth.check_password(password):
            self.bluetooth.emit(f"log-in-success:{Auth.generate_token()}")
        else:
            self.bluetooth.emit("log-in-failure")


def authenticate(operation: str):
    def wrapper(func: Callable[[str], None]):
        def wrapper(self, args: str):
            if args is None:
                self.bluetooth.emit(f"{operation}-failure:unauthorized")
                return
    
            args = args.split(", ")
            token = args.pop(0)
            args = ', '.join(args) 
            
            if len(args) == 0:
                args = None

            if Auth.check_token(token):
                func(self, args)
            else:
                self.bluetooth.emit(f"{operation}-failure:unauthorized")
        return wrapper
    return wrapper
