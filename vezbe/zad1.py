import numpy as np
import pygad

# y = f(x) = a1*x1 + a2*x2^3 + a3/x3

function_input = [13.7, -6, 25]

desired_output = 0


def fitness(solution, solution_idx):
    output = solution[0] * function_input[0] + solution[1] * \
        function_input[1]**3 + solution[2] / function_input[2]
    return -output


def on_generation(ga):
    print(ga.best_solution())


if __name__ == "__main__":
    ga = pygad.GA(
        num_generations=10,
        num_genes=3,
        init_range_low=-6,
        init_range_high=+25,
        sol_per_pop=10000,
        fitness_func=fitness,
        num_parents_mating=2,
        mutation_percent_genes=50,
        mutation_type='swap',
        on_generation=on_generation)
    ga.run()
    best_solution, best_solution_fitness, best_match_idx = ga.best_solution()
    print(best_solution)
    print(best_solution_fitness)

    ga.plot_fitness()
