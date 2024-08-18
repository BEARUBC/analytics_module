import adafruit_mcp3xxx.mcp3008 as MCP
import board
import busio
import digitalio
import logging
from typing import Generator
from adafruit_mcp3xxx.analog_in import AnalogIn
from analytics.adc.basereader import BaseAdcReader

logger = logging.getLogger(__name__)


class AdcReader(BaseAdcReader):
    def __init__(self):
        super().__init__()
        # creates the SPI bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        # creates the chip select
        cs = digitalio.DigitalInOut(board.D22)
        self._mcp = MCP.MCP3008(spi, cs)
        # create an Ananlog input channel on pin 0
        self._chan0 = AnalogIn(self._mcp, MCP.P0)
        # create an Ananlog input channel on pin 0
        self._chan1 = AnalogIn(self._mcp, MCP.P1)

    def _read_adc(self, channel) -> Generator[float, None, None]:
        while True:
            yield channel.value
