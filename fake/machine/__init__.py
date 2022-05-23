from unittest.mock import MagicMock


class UART_META:
  instance = MagicMock()
  instance.readline = MagicMock()
  instance.write = MagicMock()

  constructor = MagicMock(return_value=instance)

  def reset_mock():
    UART_META.instance.readline.reset_mock()
    UART_META.instance.write.reset_mock()
    UART_META.constructor = MagicMock(return_value=UART_META.instance)


UART = UART_META.constructor
UART.instance = UART_META.instance
UART.reset_mock = UART_META.reset_mock
UART.IRQ_TX = 1
