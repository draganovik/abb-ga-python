# traveling salesman problem

from typing import Tuple
import numpy as np
import pygad
import matplotlib.pyplot as plt

from population import *
from utils import target_distance, travel_distance
from crosswovers import cxOrderedList


def fitness(solution, solution_idx):
    index_list = solution[:n_countures-1].copy()
    target_list = solution[n_countures-1:].copy()
    for index, i in enumerate(index_list):
        if i == 0:
            distance += travel_distance(target_list[:index])
        else:
            prev_index = index_list[i-1]
            distance += travel_distance(target_list[prev_index: index])
        if i == len(index_list)-1:
            distance += travel_distance(target_list[index:])
    return -distance


def crossover(parents, chromosome_size: Tuple, ga_instance):
    childs = []
    idx = 1
    for i in range(chromosome_size[0]):
        p1_compleate = parents[i % parents.shape[0]].copy()
        p2_compleate = parents[(i+1) % parents.shape[0]].copy()
        p1 = p1_compleate[(n_countures-1):]
        p1_slices = p1_compleate[:n_countures-1]
        p2 = p2_compleate[(n_countures-1):]
        p2_slices = p2_compleate[:n_countures-1]
        p1_slices.extend(p2_slices)
        childs.append(p1_slices)
        idx += 1
    return np.array(childs)


def compleate_plot(solution):
    index_list = solution[:n_countures-1].copy()
    target_list = solution[n_countures-1:].copy()
    for index, i in enumerate(index_list):
        if i == 0:
            plt.plt(target_list[:index])
        else:
            prev_index = index_list[i-1]
            plt.plt(target_list[prev_index: index])
        if i == len(index_list)-1:
            plt.plt(target_list[index:])
    plt.plt.show()


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


def mutation(offspring, ga_inst):
    newOffspring = offspring.copy()
    target_list = newOffspring[n_countures-1:]
    index_list = newOffspring[:n_countures-1]
    size = len(target_list)
    index1 = np.random.randint(0, size)
    index2 = np.random.randint(0, size)
    if index1 > index2:
        index1, index2 = index2, index1
    target_list[index1:index2] = target_list[index2:index1:]
    probability = np.random.random_sample()
    if(probability < 0.5):
        #index_list = np.roll(index_list, 1)
        index_list = [np.clip(i+1, 0, size) for i in index_list]
    else:
        #index_list = np.roll(index_list, -1)
        index_list = [np.clip(i-1, 0, size) for i in index_list]
    index_list.extend(target_list)
    return newOffspring


if __name__ == '__main__':

    ga_instance = pygad.GA(
        initial_population=POPULATION,
        on_generation=mutation,
        num_generations=1000,
        num_parents_mating=50,
        keep_parents=10,
        gene_type=int,
        fitness_func=fitness,
        crossover_type=crossover,
        parent_selection_type='rws',
        mutation_probability=0.1,
    )

    ga_instance.run()
    best_solution, best_fitness, best_idx = ga_instance.best_solution()
    compleate_plot(best_solution)
