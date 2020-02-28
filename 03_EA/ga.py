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

    #Select the best parents for breeding
    def select_mating_pool(self, weights, fitness, no_parents):
        parents = np.empty((no_parents, weights.shape[1]))
        for parent in range(no_parents):
            lowest_fitness = np.where(fitness == np.min(fitness))
            lowest_fitness = lowest_fitness[0][0]
            parents[parent, :] = weights[lowest_fitness, :] #TODO check it later
            fitness[lowest_fitness] = -99999999999
        return parents

    def crossover(self, parents, offspring_size):

        offspring = np.empty(offspring_size)

        # The point at which crossover takes place between two parents. Usually, it is at the center.

        crossover_point = np.uint32(offspring_size[1] / 2)

        for k in range(offspring_size[0]):
            # Index of the first parent to mate.
            parent1_idx = k % parents.shape[0]

            # Index of the second parent to mate.
            parent2_idx = (k + 1) % parents.shape[0]

            # The new offspring will have its first half of its genes taken from the first parent.
            offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]

            # The new offspring will have its second half of its genes taken from the second parent.
            offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]

        return offspring

    def mutation(self, offspring_crossover, mutation_percent):

        num_mutations = np.uint32((self.mutation_prob * offspring_crossover.shape[1]) / 100) #TODO too much probably
        mutation_indices = np.array(random.sample(range(0, offspring_crossover.shape[1]), num_mutations))

        # Mutation changes a single gene in each offspring randomly.

        for idx in range(offspring_crossover.shape[0]):
            # The random value to be added to the gene.
            random_value = np.random.uniform(-1.0, 1.0, 1)
            offspring_crossover[idx, mutation_indices] = offspring_crossover[idx, mutation_indices] + random_value

        return offspring_crossover


    def calculate_fitness(self, x, y):
        return self.fitness_fuction(x,y)