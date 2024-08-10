from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_mcp3xxx.mcp3008 as MCP
import board
import busio
import digitalio

class AdcReader:
    """A class for reading values from the MCP3008 ADC
    """
    def init(
            self,
            ):
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D22)
        self._mcp = MCP.MCP3008(spi, cs)
        self._chan0 = AnalogIn(mcp, MCP.P0)

    def read(
        self
        ) -> float:
        """Read a value from the ADC

        Returns:
            float: the 10-bit value read from the ADC
        """
        # TODO: add processing to get true value. may need to do some scaling
        return self._chan0.value