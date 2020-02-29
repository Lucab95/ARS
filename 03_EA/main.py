# -*- coding: utf-8 -*-
import artificial_neural_network as ann
import genetic_algorithm as ga
import numpy as np
from math import pi, cos
import matplotlib.pyplot as plt
from matplotlib import cm


# Inputs

# FUNCTION_NAME = "Rosenbrock"  # UNTOGGLE TO CHANGE THE FUNCTION
N_PARTICLES = 5
PSO_ITERATIONS = 1000


# === Defining Benchmark Functions ===
def Rosenbrock(x, y):
    a, b = 0, 100;
    return (a - x) ** 2 + b * (y - x ** 2) ** 2;


def Rastrigin(x, y):
    return 10 * 2 + (x ** 2 - 10 * cos(2 * pi * x)) + (y ** 2 - 10 * cos(2 * pi * y))

# === define function ===
z_func = Rastrigin


# === Calculating x,y Values ===
x, y = 0, 0
LIM_m_x, LIM_M_x = -1, 1
LIM_m_y, LIM_M_y = -1, 1

if z_func.__name__ == "Rosenbrock":
    LIM_m_x, LIM_M_x = -2, 2
    LIM_m_y, LIM_M_y = -1, 3
else:  # Rastrigin
    LIM_m_x, LIM_M_x = -5, 5
    LIM_m_y, LIM_M_y = -5, 5




# == Plotting iterations ==
def GetPlottingMatrices(x, y, func):
    X, Y = np.meshgrid(x, y)
    z = np.zeros(shape=(X.shape))
    for ix in range(X.shape[0]):
        for iy in range(X.shape[0]):
            z[ix, iy] = func(X[ix, iy], Y[ix, iy])
    return X, Y, z


def PlotFunction(x, y, func):
    X, Y, z = GetPlottingMatrices(x, y, func)
    fig = plt.figure()
    ax = fig.gca()
    plt.contourf(X, Y, z, cmap=cm.jet)
    plt.colorbar(aspect=5)
    plt.xlabel('x')
    plt.ylabel('y')
    return plt, ax


def DrawMarker(ax, x, y, value, is_final_mark):
    if is_final_mark == True:
        ax.plot(x, y, color='red', marker='x', markersize=20, markeredgewidth=4)
    else:
        ax.plot(x, y, color='magenta', marker='o', markersize=5, markeredgewidth=4)
    ax.annotate(value, (x, y))


def PlottingSegment(ax, Xa, Xb, Ya, Yb):  # segment from points A to B
    ax.plot([Xa, Xb], [Ya, Yb], linewidth=1, color='black')


###################### MAIN #########################

geneticAlgorithm = ga.GeneticAlgorithm(z_func,20)
artificialNN = ann.ArtificialNeuralNetwork(2, 4, 2)
# print(GeneticEvolution.calculate_fitness(0,5))
x = np.linspace(LIM_m_x, LIM_M_x, 200)
y = np.linspace(LIM_m_y, LIM_M_y, 200)
starting_pop = ga.initialize_population(x,y)

weights=[]
for i in range(5):
    curr_vector = []
ga.select_mating_pool()
v, ax = PlotFunction(x, y, z_func)
print(starting_pop)
for i in range(len(starting_pop)):
    DrawMarker(ax,starting_pop[i][0], starting_pop[i][1],"0",False)
# NeuralNetwork = ANN(0,0,1)
v.show()

# TODO INIT VARIABLES

# TODO CREATE FIRST 50 PEOPLE (MATRIX OF MATRIX OF WEIGHTS)

# TODO CICLE FOR:
    # TODO LAUNCH ANN FOR EVERY WEIGHTS

    # TODO TAKE THEOUTPUTS AND SAVE THE ZEDS

    # TODO CHECK WHICH IS BEST N PEOPLE

    # TODO LETS MAKE FUCK THESE BEST PEOPLE AND CREATE ANOTHER 50 KIDS


# errors.append([np.square(np.subtract(x, output)).mean(), i])
# errors = np.array(errors)
# plt.plot(errors[:, 1], errors[:, 0])
# plt.xlabel('Mean square error')
# plt.ylabel('Number epochs')
# plt.show()