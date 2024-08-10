import collections

import numpy as np

# from src.AdcReader import AdcReader

class AdcBuffer:
    def __init__(
            self,
            maxLen: int = 100
            ):
        # TODO: use numpy instead?
        # TODO: support multiple channels
        # TODO: need atomic updates or thread safety
        
        # self._adc = AdcReader()
        self._q = collections.deque([], maxLen)
    
    def run(
        self
        ):
        # TODO: how to end the process? should we wait for something?
        while True:
            self._update()
        
    def read(
        self
        ) -> np.ndarray: # TODO: what kind of object are we returning?
        # TODO: what to return if buffer isnt full?
        # TODO: converting dequeue to numpy is apparently slow, is there a better way to do this?
        return np.array(self._q)
        
    def _update(
        self
        ) -> None:
        # TODO: make sure this is efficient
        # self._q.append(np.array([self._adc.read()]))
        self._q.append(np.array([9]))