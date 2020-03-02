# -*- coding: utf-8 -*-
import genetic_algorithm as ga
import plotting as plot
import numpy as np
from math import cos, pi
from copy import deepcopy
import random

# ===  Defining Benchmark Functions  ===
def Rosenbrock(x, y):  # MIN 0
    a, b = 0, 100;
    return (a - x) ** 2 + b * (y - x ** 2) ** 2
def Rastrigin(x, y):  # MIN 0
    return 10 * 2 + (x ** 2 - 10 * cos(2 * pi * x)) + (y ** 2 - 10 * cos(2 * pi * y))

# ===  INPUTS  ===

FITNESS_FUNCTION = Rastrigin  # Rosenbrock
POPULATION_SIZE = 60
PARENTS_NUMBER = POPULATION_SIZE / 5
CROSSOVER_PROBABILITY = 0.45
CROSSOVER_P_STEP = 0.3
MUTATION_PROBABILITY = 0.03
MUTATION_P_STEP = 0.01
MANTAIN_PARENTS=True


GENETIC_EPOCHS = 50
INDIVIDUAL_STEPS = 5


# ===  Calculating x,y Values  ===
LIM_m_x, LIM_M_x = -1, 1
LIM_m_y, LIM_M_y = -1, 1
if FITNESS_FUNCTION.__name__ == "Rosenbrock":
    LIM_m_x, LIM_M_x = -2, 2
    LIM_m_y, LIM_M_y = -1, 3
else:  # Rastrigin
    LIM_m_x, LIM_M_x = -5, 5
    LIM_m_y, LIM_M_y = -5, 5
x_range_list = np.linspace(LIM_m_x, LIM_M_x, 200)
y_range_list = np.linspace(LIM_m_y, LIM_M_y, 200)


# ===  MAIN  ===
Pi, Po, Z = 0, 1, 2
X, Y = 0, 1

# INITS
geneticAlgorithm = ga.GeneticAlgorithm(FITNESS_FUNCTION, CROSSOVER_PROBABILITY, CROSSOVER_P_STEP, MUTATION_PROBABILITY, MUTATION_P_STEP)
array__FF = [[[],[]],[[],[]]]  # total_average, total_stdev, best_FF, best_FF_stdev

# INIT DATASET
dataset = geneticAlgorithm.initialize_population(POPULATION_SIZE, x_range_list, y_range_list)
plot.PlottingResults(dataset, x_range_list, y_range_list, FITNESS_FUNCTION)

copied_dataset = deepcopy(dataset)
for i in range(GENETIC_EPOCHS):
    parents = geneticAlgorithm.select_parents(copied_dataset, PARENTS_NUMBER)
    copied_dataset = geneticAlgorithm.crossover_function(parents, POPULATION_SIZE, MANTAIN_PARENTS)
    copied_dataset = geneticAlgorithm.mutation_function(copied_dataset)
    if MANTAIN_PARENTS:
        all_individuals= np.empty(POPULATION_SIZE)
        all_individuals[0:PARENTS_NUMBER] = parents
        all_individuals[PARENTS_NUMBER:] = copied_dataset
        copied_dataset = deepcopy(all_individuals)
    print(copied_dataset)


#copied_dataset = deepcopy(dataset)
#for i in range(len(POPULATION_SIZE):
#    inputs = copied_dataset[i][Pi]
#    outputs = []
#    w0 = copied_dataset[i][W][0]
#    w1 = copied_dataset[i][W][1]
#    for input in inputs:
#        artificialNN.weights_0L = w0
#        artificialNN.weights_1L = w1
#        out = artificialNN.forward_propagation(input)
#        out = artificialNN.mapping_output(out, [[LIM_m_x, LIM_M_x], [LIM_m_y, LIM_M_y]])
#        outputs.append(out)
#    copied_dataset[i][Po] = outputs
#    media, stdev, rank_list_unord = geneticAlgorithm.calculate_fitness(outputs)
#    copied_dataset[i][Z] = media
#    FF_results[0].append(media)
#    FF_results[1].append(stdev)
#
#
#sorted_dataset = sorted(copied_dataset, key=lambda output: output[Z])
#
#PlottingResults(sorted_dataset[0][Po])
##PlottingResults(sorted_dataset[-1][Po])
#
##Select the best parents for breeding
#parent_list = sorted_dataset[0 : POPULATION_SAVED]
#
## make children
##children_list = geneticAlgorithm.crossover_function(parent_list, POPULATION_SIZE - POPULATION_SAVED)
##copied_dataset = parent_list + children_list
#
#plot.PlottingPerformance(FF_results)

#weights = []
#for i in range(5):
#    curr_vector = []
#ga.select_mating_pool()
#v, ax = plot.PlotFunction(x, y, FITNESS_FUNCTION)
#print(starting_pop)
#for i in range(len(starting_pop)):
#    plot.DrawMarker(ax,starting_pop[i][0], starting_pop[i][1],"0",False)
#v.show()

