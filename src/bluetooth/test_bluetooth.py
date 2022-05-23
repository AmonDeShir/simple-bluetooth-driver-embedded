from fake.fake import use_fakes
use_fakes()

from pocha import after, before_each, after_each, describe, it
from unittest.mock import MagicMock, patch
from machine import UART as UART_MOCK
import asyncio

from src.bluetooth.bluetooth import Bluetooth
from src.secret.conf import Config

@describe('Bluetooth')
def _():
    @before_each
    def _():
        UART_MOCK.reset_mock()


    @it('should send an message')
    def _():
        bluetooth = Bluetooth()
        bluetooth.send('test')
        UART_MOCK.instance.write.assert_called_with('test')


    @it('should receive an message')
    def _():
        UART_MOCK.instance.readline.return_value = 'test'
        bluetooth = Bluetooth()
        
        assert bluetooth.receive() == 'test'
    

    @describe('on')
    def _():
        @it('should call the callback when an event is received')
        def _():
            UART_MOCK.instance.readline = lambda: "test:arg1"

            func1 = MagicMock()
            bluetooth = Bluetooth()

            bluetooth.on('test', func1)

            bluetooth.listen()

            func1.assert_called_with('arg1')


        @it('should call the same callback multiple times if the event is received multiple times')
        def _():
            UART_MOCK.instance.readline = lambda: "test:arg1"

            func1 = MagicMock()
            bluetooth = Bluetooth()

            bluetooth.on('test', func1)

            bluetooth.listen()
            bluetooth.listen()
            bluetooth.listen()

            
            assert func1.call_count == 3

        
        @it('should call multiple callbacks if they are registered for the same event')
        def _():
            UART_MOCK.instance.readline = lambda: "testA"

            func1 = MagicMock()
            func2 = MagicMock()
            func3 = MagicMock()

            bluetooth = Bluetooth()

            bluetooth.on('testA', func1)
            bluetooth.on('testB', func2)
            bluetooth.on('testA', func3)

            bluetooth.listen()
            
            assert func1.call_count == 1
            assert func2.call_count == 0
            assert func3.call_count == 1


        @it('shouldn\'t call a callback if the received event is other than the event parameter of the on function')
        def _():
            UART_MOCK.instance.readline = lambda: "test"

            func1 = MagicMock()
            bluetooth = Bluetooth()

            bluetooth.on('testA', func1)

            bluetooth.listen()
            
            assert func1.call_count == 0


        @it('should call a callback with None if no argument is received')
        def _():
            UART_MOCK.instance.readline = lambda: "test"

            func1 = MagicMock()
            bluetooth = Bluetooth()

            bluetooth.on('test', func1)

            bluetooth.listen()
            
            func1.assert_called_with(None)

        
        @it('should call a callback with an argument')
        def _():
            UART_MOCK.instance.readline = lambda: "test:arg1"

            func1 = MagicMock()
            bluetooth = Bluetooth()

            bluetooth.on('test', func1)
            
            bluetooth.listen()
            
            func1.assert_called_with('arg1')