import numpy as np
import random
from scipy.spatial.distance import cdist

#seed = 1984
# np.random.seed(seed)
# random.seed(seed)


class Config:
    n_targets = 12
    n_robots = 2
    pop_size = 2000

    parents_mating = int(0.2 * pop_size)


TARGET_LIST = [
    (x, y) for x, y in zip(
        np.random.randint(10, 290, size=Config.n_targets),
        np.random.randint(10, 290, size=Config.n_targets)
    )
]
DIST_MAP = cdist(np.array(TARGET_LIST), np.array(TARGET_LIST))
# POPULATION = [
#     list(np.random.choice(list(range(Config.n_targets)), size=Config.n_targets, replace=False))
#     for _ in range(Config.pop_size)
# ]

POPULATION = []
for i in range(Config.pop_size):
    metaInfo = [np.random.randint(0, Config.n_targets)
                for _ in range(Config.n_robots-1)]
    target_list = list(np.random.choice(
        list(range(Config.n_targets)), size=Config.n_targets, replace=False))

    newChromosome = list()
    newChromosome.extend(metaInfo)
    newChromosome.extend(target_list)
    POPULATION.append(newChromosome)
