import numpy as np

np.random.seed(1234)

# TARGET CONFIG
n_targets = 12
target_low = -300
target_high = 300
n_contours = 2
# CHROMOSOME CONFIG
n_genes = n_targets

# POPULATION CONFIG
pop_size = 200

TARGETS = [(x, y) for (x, y) in zip
    (
        np.random.randint(target_low, target_high, size=n_targets),
        np.random.randint(target_low, target_high, size=n_targets)
    )
           ]

POPULATION = []

for i in range(pop_size):
    index = list(np.random.randint(0, n_targets, size = n_contours - 1))
    target_list = np.random.choice(list(range(n_targets)), size = n_targets, replace = False)
    newChromosome = list()
    newChromosome.extend(index)
    newChromosome.extend(target_list)
    POPULATION.append(newChromosome)


