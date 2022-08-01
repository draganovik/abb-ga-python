# traveling salesman problem

from typing import Tuple
import numpy as np
import pygad
import matplotlib.pyplot as plt

from population import *
from utils import target_distance, travel_distance
from crosswovers import cxOrderedList


def fitness(solution, solution_idx):
    return 1 / travel_distance(solution)


def crossover(parents, chromosome_size: Tuple, ga_instance):
    childs = []
    for i in range(chromosome_size[0]):
        p1 = parents[i % parents.shape[0]].copy()
        p2 = parents[(i+1) % parents.shape[0]].copy()
        childs.append(cxOrderedList(p1, p2))
    return np.array(childs)


def plot_solution(solution):
    x = [x for x, y in TARGETS]
    y = [y for x, y in TARGETS]
    plt.scatter(x, y)
    for it1, it2 in zip(solution[:-1], solution[1:]):
        t1 = TARGETS[it1]
        t2 = TARGETS[it2]
        x = [t1[0], t2[0]]
        y = [t1[1], t2[1]]
        plt.plot(x, y)

    start_t = solution[0]
    end_t = solution[-1]
    t1 = TARGETS[start_t]
    t2 = TARGETS[end_t]
    x = [t1[0], t2[0]]
    y = [t1[1], t2[1]]
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':

    ga_instance = pygad.GA(
        initial_population=POPULATION,
        num_generations=1000,
        num_parents_mating=50,
        keep_parents=10,
        gene_type=int,
        fitness_func=fitness,
        crossover_type=crossover,
        parent_selection_type='rws',
        # mutation_type='inversion',
        mutation_type='swap',
        mutation_probability=0.1,
    )

    ga_instance.run()
    best_solution, best_fitness, best_idx = ga_instance.best_solution()
    plot_solution(best_solution)
