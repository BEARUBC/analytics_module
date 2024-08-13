import numpy as np

class CircularList(object):
    """
    A simple implementation of a circular list. We primarily use this to buffer data in way 
    that allows us to use fixed-size buffers with efficient handling of the case when the
    buffer is full (i.e discarding oldest data without having to reallocate or traverse the
    entire buffer).
    """
    def __init__(self, size, data = []):
        self.index = 0
        self.size = size
        self._data = list(data)[-size:]

    def append(self, value):
        if len(self._data) == self.size:
            self._data[self.index] = value
        else:
            self._data.append(value)
        self.index = (self.index + 1) % self.size

    def __getitem__(self, key):
        if len(self._data) == self.size:
            return(self._data[(key + self.index) % self.size])
        else:
            return(self._data[key])

    def __repr__(self):        
        return (self._data[self.index:] + self._data[:self.index]).__repr__() + ' (' + str(len(self._data))+'/{} items)'.format(self.size)
    
    def __len__(self):
        return self.size
    
    def __array__(self) -> np.ndarray:
        """
        This method is needed to satisfy the `array-like` bound required by the 
        `np.array` method.
        """
        return np.array(self._data[self.index:] + self._data[:self.index])
