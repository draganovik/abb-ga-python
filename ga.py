import time
import pygad
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

from population import *

def single_fitness(solution):
    if len(solution) <= Config.n_targets//2 - 1:
        return 100000
    distance = DIST_MAP[solution[0], solution[-1]]

    for idx1, idx2 in zip(solution[:-1], solution[1:]):
        distance += DIST_MAP[idx1, idx2]

    return distance

def fitness(solution, solution_idx):
    totalDistance = 0
    info = solution[0:Config.n_robots - 1]  # dobijamo listu elemenata
    targets = solution[Config.n_robots - 1:]

    prevIndx = 0
    for i in info:
        subTargets = targets[prevIndx:i]
        totalDistance += single_fitness(subTargets)
        prevIndx = i

    totalDistance += single_fitness(targets[prevIndx:])

    return -totalDistance

def ocx(p1, p2, size):
    """ Ordered cycle crossover"""

    indx1 = np.random.randint(0, size)
    indx2 = np.random.randint(0, size)
    if indx2 < indx1:
        indx1, indx2 = indx2, indx1

    child = deque(p1[indx1:indx2])

    while len(child) != size:
        if p2[indx2] not in child:
            child.append(p2[indx2])
        indx2 = (indx2 + 1) % size

    child.rotate(indx1)
    return child

def crossover(parents, child_size, ga_inst):
    # child_size je tuple (broj potrebne dece, duzina jedne jedinke)
    children = []
    idx = 0
    while len(children) != child_size[0]:
        p1_with_info = parents[idx % len(parents)].copy()
        p2_with_info = parents[(idx + 1) % len(parents)].copy()
        info1 = p1_with_info[0:Config.n_robots-1]
        #info2 = p2_with_info[0:Config.n_robots-1]
        p1 = p1_with_info[Config.n_robots-1:]
        p2 = p2_with_info[Config.n_robots-1:]

        child_targets = ocx(p1, p2, len(p1))

        child = list()
        child.extend(info1)
        child.extend(child_targets)

        children.append(child)
        idx += 1

    return np.array(children)

def mutate(child, ga_inst):
    info = child[0:Config.n_robots - 1]  # dobijamo listu elemenata
    targets = child[Config.n_robots - 1:]

    id1, id2 = np.random.randint(
        0, len(targets)), np.random.randint(0, len(targets))

    targets[id1], targets[id2] = targets[id2], targets[id1]

    probability = np.random.rand()
    new_info = list()
    if probability > 0.5:
        new_info = [np.clip(0, Config.n_targets-1, i+1) for i in info]
    else:
        new_info = [np.clip(0, Config.n_targets-1, i-1) for i in info]

    mutated = list()
    mutated.extend(new_info)
    mutated.extend(targets)
    return mutated

def plot(solution):
    xs = [x for x, y in TARGET_LIST]
    ys = [y for x, y in TARGET_LIST]
    plt.scatter(xs, ys)

    for idx1, idx2 in zip(solution[:-1], solution[1:]):
        t1 = TARGET_LIST[idx1]
        t2 = TARGET_LIST[idx2]
        x1, y1 = t1
        x2, y2 = t2
        plt.plot([x1, x2], [y1, y2])

    start_idx = solution[0]
    end_idx = solution[-1]
    t1 = TARGET_LIST[start_idx]
    t2 = TARGET_LIST[end_idx]
    x1, y1 = t1
    x2, y2 = t2
    plt.plot([x1, x2], [y1, y2])

def complete_plot(solution):
    info = solution[0:Config.n_robots - 1]  # dobijamo listu elemenata
    targets = solution[Config.n_robots - 1:]

    prevIndx = 0
    for i in info:
        subTargets = targets[prevIndx:i]
        plot(subTargets)
        prevIndx = i

    plot(targets[prevIndx:])

    plt.show()

def format_sol(solution):
    info = solution[0:Config.n_robots - 1]  # dobijamo listu elemenata
    targetsIdx = solution[Config.n_robots - 1:]
    targets = [TARGET_LIST[i] for i in targetsIdx]

    sol_list = []

    prevIndx = 0
    for i in info:
        subTargets = targets[prevIndx:i]
        sol_list.append(subTargets)
        prevIndx = i

    sol_list.append(targets[prevIndx:])
    return sol_list

def get_best_solution():
    ga_instance = pygad.GA(
        num_generations=40,
        initial_population=POPULATION,
        gene_type=int,

        mutation_type=mutate,
        mutation_probability=0.5,

        # parent_selection_type="sss",
        num_parents_mating=Config.parents_mating,
        keep_parents=200,

        fitness_func=fitness,
        crossover_type=crossover
    )
    start = time.time()
    ga_instance.run()
    end = time.time()
    best_sol, best_sol_fitness, best_sol_idx = ga_instance.best_solution()

    print(f"Time: {end-start:.5f}")
    complete_plot(best_sol)
    #ga_instance.plot_fitness()

    return format_sol(best_sol)
