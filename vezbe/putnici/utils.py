import numpy as np
from population import TARGETS


def target_distance(t1, t2):
    return np.sqrt((TARGETS[t1][0] - TARGETS[t2][0])**2 + (TARGETS[t1][1] - TARGETS[t2][1])**2)


def travel_distance(target_list: list):
    if len(target_list) == 0:
        return 0
    distance = 0
    for t1, t2 in zip(target_list[:-1], target_list[1:]):
        distance += target_distance(t1, t2)
    distance += target_distance(target_list[0], target_list[-1])
    return distance
