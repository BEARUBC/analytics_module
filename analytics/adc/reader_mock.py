import logging
import random
from typing import Generator

logger = logging.getLogger(__name__)

class MockAdcReader:
    def __init__(self):
        logger.info("Initialized mock ADC reader")

    def read(self) -> Generator[tuple[float, float], None, None]:
        while True:
            yield (random.random(), random.random())