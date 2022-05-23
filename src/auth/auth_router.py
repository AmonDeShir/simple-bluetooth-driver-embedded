from requests import session
from ..bluetooth.bluetooth import Bluetooth
from .auth import Auth
from typing import Callable

class AuthRouter:
    def __init__(self, bluetooth: Bluetooth):
        self.bluetooth = bluetooth
        self.bluetooth.on("log-in", lambda args: self.log_in(args))


    def log_in(self, password: str):
        if Auth.check_password(password):
            self.bluetooth.emit(f"log-in-success:{Auth.create_session()}")
        else:
            self.bluetooth.emit("log-in-failure")


def authenticate(operation: str):
    """
    Authenticate the support staff session.
    This decorator must be used inside a Router-like class (requires self.bluetooth property).
    """

    def wrapper(func: Callable[[str], None]):
        def wrapper(self, args: str):
            if args is None:
                self.bluetooth.emit(f"{operation}-failure:unauthorized")
                return
    
            args = args.split(", ")
            session = args.pop(0)
            args = ', '.join(args) 
            
            if len(args) == 0:
                args = None

            if Auth.verify_session(session):
                func(self, args)
            else:
                self.bluetooth.emit(f"{operation}-failure:unauthorized")
        return wrapper
    return wrapper
