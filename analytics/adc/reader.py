import adafruit_mcp3xxx.mcp3008 as MCP
import board
import busio
import digitalio
import time
from adafruit_mcp3xxx.analog_in import AnalogIn
from analytics.common.circularlist import CircularList
from analytics.adc.constants import READ_BUFFER_SIZE
import logging

logger = logging.getLogger(__name__)

class AdcReader:
    def __init__(self):
        self.inner_buf = CircularList(READ_BUFFER_SIZE)
        self.outer_buf = CircularList(READ_BUFFER_SIZE)
        # creates the SPI bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        # creates the chip select
        cs = digitalio.DigitalInOut(board.D22)
        self._mcp = MCP.MCP3008(spi, cs)
        # create an Ananlog input channel on pin 0
        self._chan0 = AnalogIn(mcp, MCP.P0)
        # create an Ananlog input channel on pin 0
        self._chan1 = AnalogIn(mcp, MCP.P1)

    def start_reading(self):
        """
        Will continually read from the ADC, appending new values to the internal buffers.
        Notice that since we are using a `CircularList` type, the buffer size remains constant
        and old enough values get discarded.
        """
        random_generator = read_mock_adc()
        while True:            
            self.inner_buf.append(next(random_generator))
            self.outer_buf.append(next(random_generator))
            logger.info("Read successfully from ADC.")
            time.sleep(2)       

    def get_current_buffers(self):
        """Get current state of buffers, converted to an numpy Array"""
        inner = self.inner_buf 
        outer = self.outer_buf
        return (np.array(inner), np.array(outer))
        