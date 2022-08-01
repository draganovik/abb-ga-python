import numpy as np
import pygad

# y = f(x) = a1 * x1 + a2 * x2 + a3 * x3 + a4 * x4 + a5 * x5 + a6 * x6

function_input = [11, 0.5, -2, 4, 5.1, -16]

desired_output = 47


def fitness(solution, solution_idx):
    output = 0
    for a, x in zip(solution, function_input):
        output += a * x
    # output = np.sum(function_input * solution)
    fitness = - np.abs(desired_output - output)
    return fitness


if __name__ == "__main__":
    ga = pygad.GA(
        num_generations=20,
        num_genes=6,
        init_range_low=-5,
        init_range_high=+5,
        sol_per_pop=200,
        fitness_func=fitness,
        num_parents_mating=2,
        mutation_percent_genes=30)
    ga.run()
    best_solution, best_solution_fitness, best_match_idx = ga.best_solution()
    print(best_solution)
    print(best_solution_fitness)

    ga.plot_fitness()
    ga.plot_result()
