import random

from scipy.spatial.distance import cdist
import numpy as np

np.random.seed(100)


class Config:
    generations = 1000
    population_size = 300
    parents_mating = int(0.9 * population_size)
    keep_parents = int(0.1 * population_size)
    n_targets = 16
    n_robots = 2
    scale = 100
    xy_offset = (10, 10)

    stop_after = 100 #stop if this much generations have passed without new best fitness found

    HOME = (0, 0)


def generate_targets():
    tmp = [Config.HOME]
    xy = [(Config.xy_offset[0] + Config.scale * np.random.rand(),
           Config.xy_offset[1] + Config.scale * np.random.rand())
          for _ in range(Config.n_targets)]

    tmp.extend(xy)

    dist_matrix = cdist(xy, xy)

    return xy, dist_matrix



def generate_population(size : int, dist_matrix : cdist):

    n_targets = Config.n_targets

    population = []

    while len(population) != size:


        for i in range(n_targets):
        #first_target = np.random.randint(0, n_targets)
            newChromosome = []
            newChromosome.append(i)


            for i in range(n_targets - 1):
                next_target = newChromosome[-1]
                distance_list = dist_matrix[next_target]

                distance_pairs = [(i, d) for i, d in enumerate(distance_list) if i not in newChromosome]

                distance_pairs = sorted(distance_pairs, key = lambda tup : tup[1])
                distance_pairs = distance_pairs[:5]

                sampled_target = random.sample(distance_pairs, k=1)[0][0]

                newChromosome.append(sampled_target)


            population.append(newChromosome)
            if len(population) == size:
                break

    return population





if __name__ == "__main__":

    targets, dist_mtx = generate_targets()

    pop = generate_population(1, dist_mtx)

    print(pop)








