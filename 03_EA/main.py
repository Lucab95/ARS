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
POPULATION_SIZE = 20
POPULATION_SAVED = 25
CROSSOVER_PROBABILITY = 0.45
CROSSOVER_P_STEP = 0.3
MUTATION_PROBABILITY = 0.05
MUTATION_P_STEP = 0.01


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
x_plot = np.linspace(LIM_m_x, LIM_M_x, 200)
y_plot = np.linspace(LIM_m_y, LIM_M_y, 200)


# ===  MAIN  ===
Pi, Po, Z = 0, 1, 2
X, Y = 0, 1

# INITS
geneticAlgorithm = ga.GeneticAlgorithm(FITNESS_FUNCTION, CROSSOVER_PROBABILITY, CROSSOVER_P_STEP, MUTATION_PROBABILITY, MUTATION_P_STEP)
FF_results = [[], []]

# Creation dataset
# a vector with [[Pi],[Z]]
# Pi = [[x0,y0],..,[xn,yn]]

# INIT DATASET
dataset = []
for i in range(POPULATION_SIZE):
    x = random.choice(x_plot)
    y = random.choice(y_plot)

    dataset.append([np.array([random.choice(x_plot), random.choice(y_plot)]), []])

fitness = 10000000.

def PlottingResults(values):
    v, ax = plot.PlotFunction(x_plot, y_plot, FITNESS_FUNCTION)
    for dot in values:
        plot.DrawMarker(ax, dot[X], dot[Y], "", False)
    v.show()

PlottingResults(dataset)

copied_dataset = deepcopy(dataset)
for i in range(len(POPULATION_SIZE):
    inputs = copied_dataset[i][Pi]
    outputs = []
    w0 = copied_dataset[i][W][0]
    w1 = copied_dataset[i][W][1]
    for input in inputs:
        artificialNN.weights_0L = w0
        artificialNN.weights_1L = w1
        out = artificialNN.forward_propagation(input)
        out = artificialNN.mapping_output(out, [[LIM_m_x, LIM_M_x], [LIM_m_y, LIM_M_y]])
        outputs.append(out)
    copied_dataset[i][Po] = outputs
    media, stdev = geneticAlgorithm.calculate_fitness(outputs)
    copied_dataset[i][Z] = media
    FF_results[0].append(media)
    FF_results[1].append(stdev)


sorted_dataset = sorted(copied_dataset, key=lambda output: output[Z])

PlottingResults(sorted_dataset[0][Po])
#PlottingResults(sorted_dataset[-1][Po])

#Select the best parents for breeding
parent_list = sorted_dataset[0 : POPULATION_SAVED]

# make children
#children_list = geneticAlgorithm.crossover_function(parent_list, POPULATION_SIZE - POPULATION_SAVED)
#copied_dataset = parent_list + children_list

plot.PlottingPerformance(FF_results)

#weights = []
#for i in range(5):
#    curr_vector = []
#ga.select_mating_pool()
#v, ax = plot.PlotFunction(x, y, FITNESS_FUNCTION)
#print(starting_pop)
#for i in range(len(starting_pop)):
#    plot.DrawMarker(ax,starting_pop[i][0], starting_pop[i][1],"0",False)
## NeuralNetwork = ANN(0,0,1)
#v.show()

