import pytest
import numpy as np
from analytics.common.circularlist import CircularList

def test_constructor():
    with pytest.raises(Exception):
        CircularList(0)
    with pytest.raises(Exception):
        CircularList(-1)
    list = CircularList(1)
    assert len(list) == 1

def test_append():
    size = 3
    clist = CircularList(size)
    for i in range(size):
        clist.append(i)
    
    # should circle around once we index beyond the 
    # size
    assert clist[0] == 0
    assert clist[1] == 1
    assert clist[2] == 2
    assert clist[3] == 0
    assert clist[4] == 1
    assert clist[5] == 2

    clist.append(3)

    # should drop the oldest value (0)
    assert clist[0] == 1
    assert clist[1] == 2
    assert clist[2] == 3
    assert clist[3] == 1
    assert clist[4] == 2
    assert clist[5] == 3

def test_np_array():
    size = 3
    clist = CircularList(size)
    for i in range(size):
        clist.append(i)
    np_array = np.array(clist)

    assert type(np_array) == np.ndarray
    assert np_array.size  == size

    for i in range(size):
        assert np_array[i] == i   

    # Internally, this is now [3,1,2] -- when we convert
    # to a `np.ndarray`, we want to preserve linearity in 
    # the times items were added (i.e oldest -> newest)
    clist.append(3)
    np_array = np.array(clist)
    for i in range(size):
        assert np_array[i] == i+1




