import numpy as np

class InvalidSize(Exception):
    pass

class CircularList(object):
    """
    A simple implementation of a circular list. We primarily use this to buffer data in way 
    that allows us to use fixed-size buffers with efficient handling of the case when the
    buffer is full (i.e discarding oldest data without having to reallocate or traverse the
    entire buffer).
    """
    def __init__(self, max_size, data = []):
        if max_size <= 0:
            raise InvalidSize("A list cannot have a negative or zero maximum size.")
        self._start = len(data) if len(data) < max_size else 0
        self._max_size = max_size
        self._data = list(data)[-max_size:]

    def append(self, value) -> None:
        try:
            self._data[self._start] = value
        except IndexError as E:
            self._data.append(value)
        finally:
            self._start = (self._start + 1) % self._max_size

    def __getitem__(self, key):
        return(self._data[(key + self._start) % len(self._data)])

    def __repr__(self):        
        return (self._data[self._start:] + self._data[:self._start]).__repr__() + ' (' + str(len(self._data))+'/{} items)'.format(self._max_size)
    
    def __len__(self):
        return len(self._data)
    
    def __array__(self) -> np.ndarray:
        """
        This method is needed to satisfy the `array-like` bound required by the 
        `np.array` method.
        """
        return np.array(self._data[self._start:] + self._data[:self._start])
    
    @property
    def max_size(self) -> int:
        return self._max_size
