import random
import logging
from typing import Generator
from analytics.adc.basereader import BaseAdcReader
import numpy as np

logger = logging.getLogger(__name__)

class MockAdcReader(BaseAdcReader):
    """Mocks the AdcReader class to enable local development and testing"""
    def __init__(self):
        super().__init__()
        self._chan0 = "outer muscle"
        self._chan1 = "inner muscle"
    
    def _read_adc(self, channel) -> Generator[float, None, None]:
        burst = np.random.uniform(0, 1, size=100)
        quiet = np.random.uniform(0, 0.05, size=100)
        mock_emg_actions = {
            "activated": burst,
            "resting": quiet
        }
        while True:
            current_action = random.choice(list(mock_emg_actions))
            logger.info(f"Pilot's {channel} is currently in state={current_action}")
            for i in mock_emg_actions[current_action]:
                yield i


