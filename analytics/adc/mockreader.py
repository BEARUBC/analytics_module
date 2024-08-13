import random
import logging
from typing import Generator
from analytics.adc.basereader import BaseAdcReader

logger = logging.getLogger(__name__)

class MockAdcReader(BaseAdcReader):
    """Mocks the AdcReader class to enable local development and testing"""
    def __init__(self):
        super().__init__()
    
    def _read_adc(self, _) -> Generator[float, None, None]:
        while True:
            # TODO: @krarpit read from real data values in the `data` directory
            yield random.random() # yields a random number between 0.0 and 1.0


