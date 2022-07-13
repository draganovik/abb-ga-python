import pygad
import numpy as np
import matplotlib.pyplot as plt

from population import *
from crossovers import cxOrderedList
from utils import target_distance, travel_distance


def fitness(solution, solution_idx):
    index_list = solution[:n_contours-1].copy()
    target_list = solution[n_contours-1:].copy()

    distance = 0
    for i, index in enumerate(index_list):
        if i == 0:
            distance += travel_distance(target_list[:index])
        else:
            prev_index = index[i-1]
            distance += travel_distance(target_list[prev_index : index])

        if i == len(index_list) - 1:
            distance += travel_distance(target_list[index:])


    return  -distance


def crossover(parents, chromosome_size, ga_inst):
    # chromosome_size je tuple (size_1, size_2)
    # size_1 : potreban broj novih jedinki
    # size_2 : duzina svake jedinke
    # return mora biti np.array

    children = []
    idx = 0
    while len(children) != chromosome_size[0]:
        p1_complete = parents[idx % parents.shape[0]].copy()
        p2_complete = parents[(idx + 1) % parents.shape[0]].copy()
        p1 = p1_complete[(n_contours - 1):]
        p1_slices = list(p1_complete[:n_contours - 1])

        p2 = p2_complete[(n_contours - 1):]
        p2_slices = p2_complete[:n_contours - 1]

        child = cxOrderedList(p1, p2)
        p1_slices.extend(child)

        children.append(p1_slices)
        idx += 1

    return np.array(children)


def mutation(offspring, ga_inst):
    """ offspring je list, pa je mutabilna i mozemo ga direktno menjati"""
    newOffspring = offspring.copy()

    target_list = newOffspring[n_contours - 1:]
    index_list = newOffspring[:n_contours - 1]

    size = len(target_list)
    indx1 = np.random.randint(0, size)
    indx2 = np.random.randint(0, size)
    if indx1 > indx2:
        indx1, indx2 = indx2, indx1
    target_list[indx1:indx2] = target_list[indx2:indx1]

    probability = np.random.random_sample()
    if probability > 0.5:
        index_list = [np.clip(i + 1, 0, size) for i in index_list]
    else:
        index_list = [np.clip(i - 1, 0, size) for i in index_list]

    index_list.extend(target_list)
    return index_list


def plot(solution):
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

    #plt.show()

def compete_plot(final_solution):
    index_list = final_solution[:n_contours - 1].copy()
    target_list = final_solution[n_contours - 1:].copy()

    for i, index in enumerate(index_list):
        if i == 0:
            plot(target_list[:index])
        else:
            prev_index = index[i - 1]
            plot(target_list[:index])

        if i == len(index) - 1:
            plot(target_list[:index])

    plt.show()

def on_generation(ga_instance : pygad.GA):
    print(ga_instance.num_generations)

if __name__ == "__main__":
    ga_instance = pygad.GA(
        initial_population=POPULATION,
        num_generations=200,
        num_parents_mating=50,
        keep_parents=10,

        gene_type=int,
        fitness_func=fitness,
        crossover_type=crossover,
        on_generation = on_generation,
        parent_selection_type="rws",

        # mutation_type="inversion",
        mutation_probability=0.1
    )

    ga_instance.run()
    best_solution, best_fitness, best_idx = ga_instance.best_solution()

    compete_plot(best_solution)
    # ga_instance.plot_fitness()
