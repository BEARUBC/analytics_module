import time 
import logging
from analytics.common.circularlist import CircularList
from typing import Generator
from analytics import config
import numpy as np
from abc import ABC, abstractmethod
from analytics.common.backoff import exponential_backoff_decorator

logger = logging.getLogger(__name__)

class BufferNotFull(Exception):
    pass

class BaseAdcReader(ABC):
    """Base class encapsulating shared logic for the real and mock ADC readers"""
    def __init__(self):
        self.config = config["adc"]
        logger.info(f"ADC reader configs: {self.config}")
        self._inner_read_buffer_size = self.config["inner_read_buffer_size"].as_number()
        self._outer_read_buffer_size = self.config["outer_read_buffer_size"].as_number()
        self._sleep_duration = self.config["sleep_between_reads_in_seconds"].as_number()
        self.inner_buf = CircularList(self._inner_read_buffer_size)
        self.outer_buf = CircularList(self._outer_read_buffer_size)
        self._chan0 = None
        self._chan1 = None

    def start_reading(self):
        """
        Will continually read from the ADC, appending new values to the internal buffers.
        Notice that since we are using a `CircularList` type, the buffer size remains constant
        and old enough values get discarded.
        """
        inner_adc_value = self._read_adc(self._chan0)
        outer_adc_value = self._read_adc(self._chan1)
        logger.info("Starting to read ADC values for both inner and outer muscles.")
        while True:            
            self.inner_buf.append(next(inner_adc_value))
            self.outer_buf.append(next(outer_adc_value)) 
            time.sleep(self._sleep_duration)      
    
    @abstractmethod
    def _read_adc(self, channel) -> Generator[float, None, None]:
        None

    @exponential_backoff_decorator(base_delay_in_seconds=0.1, logger=logger)
    def get_current_buffers(self):
        """Get current state of buffers, converted to an numpy Array"""
        inner, outer = self.inner_buf, self.outer_buf
        if (not inner.is_full() or not outer.is_full()):
            raise BufferNotFull("At least one of the buffers is not full yet")
        return (np.array(inner), np.array(outer))
