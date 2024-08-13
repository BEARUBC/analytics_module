import random
import time 
import logging
from analytics.common.circularlist import CircularList
from analytics.adc.constants import READ_BUFFER_SIZE
from typing import Generator
import numpy as np


logger = logging.getLogger(__name__)

def read_mock_adc() -> Generator[float, None, None]:
    while True:
        yield random.random()

class MockAdcReader:
    def __init__(self):
        self.inner_buffer = CircularList(READ_BUFFER_SIZE)
        self.outer_buffer = CircularList(READ_BUFFER_SIZE)

    def start_reading(self):
        random_generator = read_mock_adc()
        while True:
            self.inner_buffer.append(next(random_generator))
            self.outer_buffer.append(next(random_generator))
            # logger.info(f"Read from the ADC: inner_buffer={self.inner_buffer} outer_buffer={self.outer_buffer}")
            time.sleep(2)       

    def get_current_buffers(self):
        logger.info(f"{self.inner_buffer}, {self.outer_buffer}")
        (np.array(self.inner_buffer), np.array(self.outer_buffer))

