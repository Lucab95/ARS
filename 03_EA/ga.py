import numpy as np
import random

class Ga:
    def __init__(self, function_name, pop_size =50, crossover_prob = 0.45, crossover_prob_step = 0.3, mutation_prob = 0.05, mutation_prob_step = 0.01):
        self.pop_size= pop_size
        self.crossover_prob = crossover_prob
        self.crossover_prob_step = crossover_prob_step
        self.mutation_prob = mutation_prob
        self.mutation_prob_step = mutation_prob_step
        self.fitness_fuction= function_name

    def initialize_population(self, x, y):
        population = []
        for i in range(self.pop_size):
            population.append(np.array([random.choice(x), random.choice(y)]))
        return np.array(population)

    def calculate_fitness(self, x, y):
           return self.fitness_fuction(x,y)