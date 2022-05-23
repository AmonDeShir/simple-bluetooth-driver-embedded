from ..bluetooth.bluetooth import Bluetooth
from ..auth.auth_router import authenticate
from typing import Callable

class LoggerRouter:
    def __init__(self, bluetooth: Bluetooth):
        self.bluetooth = bluetooth
        self.bluetooth.on("test_a", lambda args: self.test_a(args))
        self.bluetooth.on("test_b", lambda args: self.test_b(args))


    def test_a(self):
        self.bluetooth.emit("test-data")


    @authenticate("test_b")
    def test_b(self):
        self.bluetooth.emit("test-data")