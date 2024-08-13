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
        self.inner_buf = CircularList(READ_BUFFER_SIZE)
        self.outer_buf = CircularList(READ_BUFFER_SIZE)

    def start_reading(self):
        random_generator = read_mock_adc()
        while True:
            self.inner_buf.append(next(random_generator))
            self.outer_buf.append(next(random_generator))
            time.sleep(2)       

    def get_current_buffers(self):
        inner = self.inner_buf 
        outer = self.outer_buf
        return (np.array(inner), np.array(outer))

