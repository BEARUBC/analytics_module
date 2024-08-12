import adafruit_mcp3xxx.mcp3008 as MCP
import board
import busio
import digitalio
from adafruit_mcp3xxx.analog_in import AnalogIn
from typing import Generator

class AdcReader:
    def __init__(self):
        # creates the SPI bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        # creates the chip select
        cs = digitalio.DigitalInOut(board.D22)
        self._mcp = MCP.MCP3008(spi, cs)
        # create an Ananlog input channel on pin 0
        self._chan0 = AnalogIn(mcp, MCP.P0)
        # create an Ananlog input channel on pin 0
        self._chan1 = AnalogIn(mcp, MCP.P1)

    def read(self) -> Generator[tuple[float, float], None, None]:
        while True:
            yield (self._chan0.value, self._chan1.value)