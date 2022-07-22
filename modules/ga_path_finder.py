import numpy as np
import random
import math
import matplotlib.pyplot as plt
from ga_globals import *
'''
Genetical path finding
Finds locally best ways from L starting points with [M0, M1, ..., ML] robots
through points_number Points and back to their service center
'''


def fitness_pop(population, dist, robots):
    fitness_result = np.zeros(len(population))
    for i in range(len(fitness_result)):
        fitness_result[i] = fitness(population[i], dist, robots)
    return fitness_result


def fitness(creature, dist, robots):
    sum_dist = np.zeros(len(creature))
    for j in range(len(creature)):
        mat_path = np.zeros((dist.shape[0], dist.shape[1]))
        path = creature[j]
        if len(path) != 0:
            for v in range(len(path)):
                if v == 0:
                    mat_path[robots[j], path[v]] = 1
                else:
                    mat_path[path[v - 1] + starting_points, path[v]] = 1
            mat_path = mat_path * dist
            sum_dist[j] = (np.sum(mat_path) + dist[robots[j],
                           path[-1]]) / velocity + repair_time * len(path)
    return np.max(sum_dist) + np.average(sum_dist) / len(creature)


def birth_prob(fitness_result):
    birth_prob = np.abs(fitness_result - np.max(fitness_result))
    if(np.sum(birth_prob) == 0):
        return np.zeros(len(birth_prob)) * 1
    birth_prob = birth_prob / np.sum(birth_prob)
    return birth_prob


def mutate(creat, robo):
    pnt_1 = random.randint(0, len(creat)-1)
    pnt_2 = random.randint(0, len(creat)-1)
    if random.random() < mut_1_prob:
        creat[pnt_1], creat[pnt_2] = creat[pnt_2], creat[pnt_1]
    if random.random() < mut_2_prob and pnt_1 != pnt_2:
        if pnt_1 > pnt_2:
            pnt_1, pnt_2 = pnt_2, pnt_1
        creat[pnt_1:pnt_2+1] = list(reversed(creat[pnt_1:pnt_2+1]))
    if random.random() < mut_3_prob:
        #robo = [number-1 for number in robo if number != 0]
        robo = [number - 2 for number in robo if number != 0]
        while(sum(robo) != points_number):
            robo[random.randint(0, len(robo)-1)] += 1
    return creat, robo


def crossover_mutation(population, birth_prob, dist, robots):
    new_population = []
    for i in range(round(len(population)/2)):
        prob = np.random.rand(birth_prob.size) - birth_prob
        pair = np.zeros(2).astype(int)
        pair[0] = np.argmin(prob)
        pair[1] = random.randint(0, prob.size-1)
        robo_1 = [len(population[pair[0]][v])
                  for v in range(len(population[pair[0]]))]
        robo_2 = [len(population[pair[1]][v])
                  for v in range(len(population[pair[1]]))]
        parent_1 = []
        parent_2 = []
        for j in range(len(robo_1)):
            parent_1 += population[pair[0]][j]
        for j in range(len(robo_2)):
            parent_2 += population[pair[1]][j]
        creat_1 = [-1] * len(parent_1)
        creat_2 = [-1] * len(parent_2)
        cross_point_1 = random.randint(0, len(parent_1) - 1)
        cross_point_2 = random.randint(0, len(parent_2) - 1)
        node_1 = parent_1[cross_point_1:]
        node_2 = parent_2[cross_point_2:]
        w = 0
        for v in range(len(creat_1)):
            if parent_2[v] not in node_1:
                creat_1[v] = parent_2[v]
            else:
                creat_1[v] = node_1[w]
                w += 1
        w = 0
        for v in range(len(creat_2)):
            if parent_1[v] not in node_2:
                creat_2[v] = parent_1[v]
            else:
                creat_2[v] = node_2[w]
                w += 1
        # mutations
        creat_1, robo_1 = mutate(creat_1, robo_1)
        creat_2, robo_2 = mutate(creat_2, robo_2)
        # children
        child_1 = []
        robo_sum = 0
        for v in range(len(robo_1)):
            child_1.append(creat_1[robo_sum:robo_sum+robo_1[v]])
            robo_sum += robo_1[v]
        child_2 = []
        robo_sum = 0
        for v in range(len(robo_2)):
            child_2.append(creat_2[robo_sum:robo_sum + robo_2[v]])
            robo_sum += robo_2[v]
        together = [child_1, child_2, population[pair[0]], population[pair[1]]]
        fit = np.array([fitness(creature, dist, robots)
                       for creature in together])
        fit = fit.argsort()
        new_population.append(together[fit[0]])
        new_population.append(together[fit[1]])
    return new_population


def plot_paths(paths, points_locations, robots):
    plt.clf()
    plt.title('Best path overall')
    for v in range(starting_points):
        plt.scatter(points_locations[v, 0], points_locations[v, 1], c='r')
    for v in range(points_number):
        plt.scatter(points_locations[v+starting_points, 0],
                    points_locations[v+starting_points, 1], c='b')
    for v in range(len(paths)):
        if len(paths[v]) != 0:
            path_locations = points_locations[starting_points:]
            path_locations = path_locations[np.array(paths[v])]
            path_locations = np.vstack(
                (points_locations[robots[v]], path_locations))
            path_locations = np.vstack(
                (path_locations, points_locations[robots[v]]))
            plt.plot(path_locations[:, 0], path_locations[:, 1])
    plt.show()
    plt.pause(0.000001)


def create_robots():
    robots = []

    for i in range(starting_points):
        for _ in range(random.randint(1, max_robo)):
            robots.append(i)

    robots = np.array(robots)
    print('robots: {}'.format(robots))
    return robots


def create_population(robots):
    population = []
    for i in range(population_size):
        points_range = list(range(points_number))
        pop = [0] * robots.size
        for j in range(robots.size):
            pop[j] = []
            if len(points_range) != 0:
                if j != robots.size-1:
                    for v in range(random.randint(1, round(2*points_number/robots.size))):
                        pop[j].append(random.choice(points_range))
                        points_range.remove(pop[j][-1])
                        if len(points_range) == 0:
                            break
                else:
                    for v in range(len(points_range)):
                        pop[j].append(random.choice(points_range))
                        points_range.remove(pop[j][-1])
        population.append(pop)
    return population


def main():
    plt.ion()

    robots = create_robots()

    dist = np.zeros((points_number+starting_points, points_number))

    points_locations = np.random.randint(
        0, 300, (starting_points+points_number)*2)

    points_locations = points_locations.reshape(
        (starting_points+points_number, 2))

    for i in range(dist.shape[0]):
        for j in range(dist.shape[1]):
            dist[i, j] = math.sqrt((points_locations[i, 0] - points_locations[j + starting_points, 0]) ** 2 +
                                   (points_locations[i, 1] - points_locations[j + starting_points, 1]) ** 2)
            if j+starting_points == i:
                dist[i][j] = 0
    # random population creation
    population = create_population(robots)
    fitness_result = fitness_pop(population, dist, robots)
    best_mean_creature_result = np.mean(fitness_result)
    best_creature_result = np.min(fitness_result)
    best_selection_prob = birth_prob(fitness_result)
    selection_prob = best_selection_prob
    new_population = population.copy()
    plot_paths(population[np.argmin(fitness_result)],
               points_locations, robots)
    for i in range(generations):
        new_population = crossover_mutation(
            population, selection_prob, dist, robots)
        fitness_result = fitness_pop(new_population, dist, robots)
        mean_creature_result = np.mean(fitness_result)
        if np.min(fitness_result) < best_creature_result:
            plot_paths(population[np.argmin(fitness_result)],
                       points_locations, robots)
            best_creature_result = np.min(fitness_result)
        if mean_creature_result < best_mean_creature_result:
            best_mean_creature_result = mean_creature_result
            best_selection_prob = birth_prob(fitness_result)
            selection_prob = best_selection_prob
            population = new_population.copy()
        print('Mean population time: {0} Best time: {1}'.format(
            best_mean_creature_result, best_creature_result))
    plt.ioff()
    plt.show()
    # print paths
    print('Best path: {}'.format(population[np.argmin(fitness_result)]))
    points_solution_indexes = population[np.argmin(fitness_result)]
    points_solution = [[], []]
    for i in range(len(points_solution_indexes)):
        for j in range(len(points_solution_indexes[i])):
            points_solution[i].append(
                points_locations[points_solution_indexes[i][j]])
    print(np.array(points_solution))


if __name__ == '__main__':
    main()
