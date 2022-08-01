from collections import deque
import numpy as np


def cxOrderedList(p1, p2):
    assert len(p1) == len(p2), 'Roditelji nosi iste duzine'
    idx1, idx2 = np.random.randint(0, len(p1), size=2)
    if idx1 > idx2:
        idx1, idx2 = idx2, idx1

    child = deque(p1[idx1:idx2])

    while len(child) != len(p1):
        if p2[idx2] not in child:
            child.append(p2[idx2])
        idx2 = (idx2 + 1) % len(p2)
    child.rotate(idx1)

    return np.array(child)
