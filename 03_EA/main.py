# -*- coding: utf-8 -*-
import artificial_neural_network as ann
import genetic_algorithm as ga
import plotting as plot
import numpy as np
from math import pi, cos


# ===  Defining Benchmark Functions  ===
def Rosenbrock(x, y):
    a, b = 0, 100;
    return (a - x) ** 2 + b * (y - x ** 2) ** 2
def Rastrigin(x, y):
    return 10 * 2 + (x ** 2 - 10 * cos(2 * pi * x)) + (y ** 2 - 10 * cos(2 * pi * y))


# ===  INPUTS  ===
POPULATION_SIZE = 5
GENETIC_EPOCHS = 50
INDIVIDUAL_STEPS = 5
FITNESS_FUNCTION = Rastrigin  # Rosenbrock


# ===  Calculating x,y Values  ===
x, y = 0, 0
LIM_m_x, LIM_M_x = -1, 1
LIM_m_y, LIM_M_y = -1, 1
if FITNESS_FUNCTION.__name__ == "Rosenbrock":
    LIM_m_x, LIM_M_x = -2, 2
    LIM_m_y, LIM_M_y = -1, 3
else:  # Rastrigin
    LIM_m_x, LIM_M_x = -5, 5
    LIM_m_y, LIM_M_y = -5, 5


# ===  MAIN  ===

geneticAlgorithm = ga.GeneticAlgorithm(FITNESS_FUNCTION, 20)
artificialNN = ann.ArtificialNeuralNetwork(2, 4, 2)
# print(GeneticEvolution.calculate_fitness(0,5))
x = np.linspace(LIM_m_x, LIM_M_x, 200)
y = np.linspace(LIM_m_y, LIM_M_y, 200)
starting_pop = ga.initialize_population(x,y)

weights=[]
for i in range(5):
    curr_vector = []
ga.select_mating_pool()
v, ax = plot.PlotFunction(x, y, FITNESS_FUNCTION)
print(starting_pop)
for i in range(len(starting_pop)):
    plot.DrawMarker(ax,starting_pop[i][0], starting_pop[i][1],"0",False)
# NeuralNetwork = ANN(0,0,1)
v.show()

# TODO INIT VARIABLES

# TODO CREATE FIRST 50 PEOPLE (MATRIX OF MATRIX OF WEIGHTS)

# TODO CICLE FOR:
    # TODO LAUNCH ANN FOR EVERY WEIGHTS

    # TODO TAKE THEOUTPUTS AND SAVE THE ZEDS

    # TODO CHECK WHICH IS BEST N PEOPLE

    # TODO LETS MAKE FUCK THESE BEST PEOPLE AND CREATE ANOTHER 50 KIDS