import numpy as np

np.random.seed(666)

# TARGET CONFIG
n_targets = 12
target_low = 0
target_high = 300
n_countures = 2

# CHROMOSOME CONFIG
n_genes = n_targets

# POPULATION CONFIG
pop_size = 200

TARGETS = [(x, y) for (x, y) in zip(
    np.random.randint(target_low, target_high, size=n_targets),
    np.random.randint(target_low, target_high, size=n_targets))]

POPULATION = []

for i in range(pop_size):
    index = np.random.randint(0, n_targets, size=n_countures - 1)
    target_list = np.random.choice(
        list(range(n_targets)), size=n_targets, replace=False)
    newChromosome = list()
    newChromosome.extend(index)
    newChromosome.extend(target_list)
    POPULATION.append(newChromosome)

COMPLEATE_POPULATION = []

for c in POPULATION:
    newPair = {
        'chromosome': c,
        'slices': (i for i in np.random.randint(0, n_targets, size=n_countures - 1)),
    }
    COMPLEATE_POPULATION.append(newPair)
