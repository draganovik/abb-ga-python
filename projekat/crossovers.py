from collections import deque

import numpy as np


def cxOrderedList(p1, p2):

    assert len(p1) == len(p2), "Roditelji nisu iste duzine"

    parent_size = len(p1)

    idx1, idx2 = np.random.randint(0, parent_size), np.random.randint(0, parent_size)

    if (idx1 > idx2):
        idx1, idx2 = idx2, idx1

    child = deque(p1[idx1:idx2])

    while len(child) != parent_size:
        if p2[idx2] not in child:
            child.append(p2[idx2])
        idx2 = (idx2 + 1) % parent_size

    child.rotate(idx1)

    return child


