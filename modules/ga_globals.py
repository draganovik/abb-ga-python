# seed
# np.random.seed(21)
# random.seed(1)

# Bank parameters
points_number = 12         # Point quantity
starting_points = 2    # starting points quantity
max_robo = 2           # number of robots

velocity = 1            # 100 / hour
repair_time = 2         # 0.5 hour


# genetic parameters
population_size = 900    # population size (even number!)
generations = 100       # population's generations
mut_1_prob = 0.15         # prob of replacing together two points in combined path
mut_2_prob = 0.2     # prob of reversing the sublist in combined path
mut_3_prob = 0.25     # probability of changing the length of paths for robots
two_opt_search = True  # better convergence, lower speed for large quantity of points
