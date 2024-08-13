import random
import time 
import logging
from analytics.common.circularlist import CircularList
from analytics.adc.constants import READ_BUFFER_SIZE
from typing import Generator
import numpy as np

logger = logging.getLogger(__name__)

def read_mock_adc() -> Generator[float, None, None]:
    """Returns a stream of random ADC values (between 0.0 and 1.0)"""
    while True:
        yield random.random()

class MockAdcReader:
    """Mocks the AdcReader class to enable local development and testing"""
    def __init__(self):
        self.inner_buf = CircularList(READ_BUFFER_SIZE)
        self.outer_buf = CircularList(READ_BUFFER_SIZE)

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

