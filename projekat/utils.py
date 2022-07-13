import numpy as np
from population import TARGETS

def target_distance(t1, t2) -> float:
    x1, y1 = TARGETS[t1]
    x2, y2 = TARGETS[t2]
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def travel_distance(target_list: list):
    if len(target_list) == 0:
        return 0

    distance = 0

    start_target = target_list[0]
    end_target = target_list[-1]

    for t1, t2 in zip(target_list[:-1], target_list[1:]):
        distance += target_distance(t1, t2)

    distance += target_distance(start_target, end_target)

    return distance
