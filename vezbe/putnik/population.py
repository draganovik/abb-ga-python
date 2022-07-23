import numpy as np

np.random.seed(666)


# TARGET CONFIG
n_targets = 12
target_low = 0
target_high = 300

# CHROMOSOME CONFIG
n_genes = n_targets

# POPULATION CONFIG
pop_size = 200

TARGETS = [(x, y) for (x, y) in zip(
    np.random.randint(target_low, target_high, size=n_targets),
    np.random.randint(target_low, target_high, size=n_targets))]

POPULATION = []

for i in range(pop_size):
    newChromosome = np.random.choice(
        list(range(n_targets)), size=n_targets, replace=False)
    POPULATION.append(newChromosome)
