# -*- coding: utf-8 -*-
import artificial_neural_network as ann
import genetic_algorithm as ga
import plotting as plot
import numpy as np
from math import cos, pi
from copy import deepcopy


# ===  Defining Benchmark Functions  ===
def Rosenbrock(x, y):
    a, b = 0, 100;
    return (a - x) ** 2 + b * (y - x ** 2) ** 2
def Rastrigin(x, y):
    return 10 * 2 + (x ** 2 - 10 * cos(2 * pi * x)) + (y ** 2 - 10 * cos(2 * pi * y))


# ===  INPUTS  ===
# == ANN ==
ANN_INPUT_SIZE = 2
ANN_HIDDEN_LAYER_SIZE = 4
ANN_OUTPUT_SIZE = 2

# == GA ==
FITNESS_FUNCTION = Rastrigin  # Rosenbrock
POPULATION_SIZE = 50
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
Pi, Po, W, Z = 0, 1, 2, 3
X, Y = 0, 1

# INITS
geneticAlgorithm = ga.GeneticAlgorithm(FITNESS_FUNCTION, POPULATION_SIZE, CROSSOVER_PROBABILITY, CROSSOVER_P_STEP, MUTATION_PROBABILITY, MUTATION_P_STEP)
artificialNN = ann.ArtificialNeuralNetwork(ANN_INPUT_SIZE, ANN_HIDDEN_LAYER_SIZE, ANN_OUTPUT_SIZE)

# Creation dataset
# a vector with [[Pi],[Po],[W0, W1][Z]]
# Pi = [[x0,y0],..,[xn,yn]] and so is Po
dataset = []
# inputs
inputs = [
    [3, 0],
    [0, 3],
    [-3, 0],
    [0, -3],
]

fitness = 10000000.

def PlottingResults(values):
    v, ax = plot.PlotFunction(x_plot, y_plot, FITNESS_FUNCTION)
    for dot in values:
        plot.DrawMarker(ax, dot[X], dot[Y], "", False)
    v.show()

PlottingResults(inputs)

# outputs
outputs = []
# weights
for i in range(POPULATION_SIZE):
    W1 = np.random.randn(ANN_INPUT_SIZE, ANN_HIDDEN_LAYER_SIZE)
    W2 = np.random.randn(ANN_HIDDEN_LAYER_SIZE, ANN_OUTPUT_SIZE)
    new_element = [inputs, outputs, [W1, W2], fitness]
    dataset.append(new_element)


copied_dataset = deepcopy(dataset)
for i in range(POPULATION_SIZE):
    inputs = copied_dataset[i][Pi]
    outputs = []
    w0 = copied_dataset[i][W][0]
    w1 = copied_dataset[i][W][1]
    for input in inputs:
        artificialNN.weights_1L = w0
        artificialNN.weights_2L = w1
        out = artificialNN.forward_propagation(input)
        out = artificialNN.mapping_output(out, [[LIM_m_x, LIM_M_x], [LIM_m_y, LIM_M_y]])
        outputs.append(out)
    copied_dataset[i][Po] = outputs
    copied_dataset[i][Z] = geneticAlgorithm.calculate_fitness(outputs)


sorted_dataset = sorted(copied_dataset, key=lambda output: output[Z])

PlottingResults(sorted_dataset[0][Po])
#PlottingResults(sorted_dataset[-1][Po])

parent_list = sorted_dataset[0:POPULATION_SAVED]

#TODO from now the copied_dataset has Poutputs and random weights

#starting_pop = ga.initialize_population(x, y)

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

# TODO CICLE FOR:

    # TODO LAUNCH ANN FOR EVERY WEIGHTS

    # TODO TAKE THEOUTPUTS AND SAVE THE ZEDS

    # TODO CHECK WHICH IS BEST N PEOPLE
