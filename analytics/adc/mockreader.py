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
        self._buffer_size = self.config["mock_reader_state_buffer_size"].as_number()
    
    def _read_adc(self, _) -> Generator[float, None, None]:
        burst = np.random.uniform(-1, 1, size=self._buffer_size)
        quiet = np.random.uniform(-0.05, 0.05, size=self._buffer_size)
        mock_emg_actions = {
            "activated": burst,
            "resting": quiet
        }
        while True:
            current_action = random.choice(list(mock_emg_actions))
            # logger.info(f"Pilot's {channel} is currently in state={current_action}")
            for i in mock_emg_actions[current_action]:
                yield i


