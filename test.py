import pygad
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from crossovers import *

seed = 99
np.random.seed(seed)
random.seed(seed)

TARGETS, DIST_MATRIX = generate_targets()
POPULATION = generate_population(Config.population_size, DIST_MATRIX)
current_gen = 0

def get_target_distance(t1, t2):
    x1, y1 = t1
    x2, y2 = t2
    dist = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return dist

def fitness_function(solution, solution_idx):
    distances = get_target_distance(Config.HOME, TARGETS[solution[0]])

    for i1, i2 in zip(solution[:-1], solution[1:]):
       distances += DIST_MATRIX[i1][i2]

    distances += get_target_distance(Config.HOME, TARGETS[solution[-1]])

    return -distances


def crossover_function(parents, offspring_size, ga_inst: pygad.GA):
    offspring = []
    idx = 0

    while len(offspring) != offspring_size[0]:
        parent1 = parents[idx % parents.shape[0], :].copy()
        parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

        c1 = cxPartialyMatched(parent1, parent2)

        offspring.append(c1)

        idx += 1

    return np.array(offspring)


def on_gen(ga: pygad.GA):
    global current_gen
    current_gen += 1
    best, fitness, _ = ga.best_solution()
    print("-" * 50)
    print(f"Generation [{current_gen}]: \nSolution:{best} \nFitness: {fitness}")


def plot_solution(solution):
    line_pairs = []

    xs = [t[0] for t in TARGETS]
    ys = [t[1] for t in TARGETS]
    xs.append(0)
    ys.append(0)

    plt.scatter(xs, ys)

    # PLOT FROM HOME LINE
    p1 = Config.HOME
    p2 = TARGETS[solution[0]]
    x = [p1[0], p2[0]]
    y = [p1[1], p2[1]]
    plt.plot(x, y)

    for i in range(len(solution) - 1):
        p1 = TARGETS[solution[i]]
        p2 = TARGETS[solution[i + 1]]
        x = [p1[0], p2[0]]
        y = [p1[1], p2[1]]
        plt.plot(x, y)

    # PLOT TO HOME LINE
    p1 = Config.HOME
    p2 = TARGETS[solution[-1]]
    x = [p1[0], p2[0]]
    y = [p1[1], p2[1]]
    plt.plot(x, y)

    plt.show()


if __name__ == "__main__":
    ga_instance = pygad.GA(
        num_generations=Config.generations,
        num_parents_mating=Config.parents_mating,  # total number of parents to mate
        keep_parents=Config.keep_parents,

        fitness_func=fitness_function,

        initial_population= POPULATION,
        #sol_per_pop=Config.population_size,
        #num_genes=Config.n_targets,
        gene_type=int,

        init_range_low=0,
        init_range_high=Config.n_targets,

        parent_selection_type="rws",
        # K_tournament=int(0.1 * Config.population_size),  # 10% of population size
        crossover_type=crossover_function,

        mutation_type="inversion",
        mutation_probability=0.05,  # chance to swap two random genes

        # save_solutions=True,
        #save_best_solutions=True,
        allow_duplicate_genes=False,
        stop_criteria=f"saturate_{Config.stop_after}",

        #on_generation=on_gen
    )
    ga_instance.run()
    best_solution, best_fitness, best_index = ga_instance.best_solution()
    ga_instance.plot_fitness()
    print(f"Best solution: {best_solution}")
    print(f"Best fitness: {best_fitness}")

    plot_solution(best_solution)
