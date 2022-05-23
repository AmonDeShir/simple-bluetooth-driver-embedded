from machine import UART
from src.secret.conf import Config
from typing import Callable

class Bluetooth:
    def __init__(self):
        self.events = dict()
        self.uart = UART(Config.bluetooth_uart, 9600)


    def listen(self):
        msg = self.receive()
            
        if not msg is None:
            self._eventQueue(msg.split(":"))


    def _eventQueue(self, msg):
        key = msg[0]
        args = msg[1] if len(msg) > 1 else None

        for event in self.events:
            if event == key:
                for callback in self.events[key]:
                    callback(args)


    def send(self, data):
        self.uart.write(data)


    def receive(self):
        return self.uart.readline()


    def on(self, event: str, callback: Callable[[str, str], None]):
        if not event in self.events.keys():
            self.events[event] = []

        self.events[event].append(callback)
