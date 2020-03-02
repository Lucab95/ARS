import numpy as np
import random
import statistics as stats

X, Y, Z = 0, 1, 2


class GeneticAlgorithm:

    def __init__(self, function_name, crossover_prob, crossover_prob_step, mutation_prob, mutation_prob_step):
        self.crossover_prob = crossover_prob
        self.crossover_prob_step = crossover_prob_step
        self.mutation_prob = mutation_prob
        self.mutation_prob_step = mutation_prob_step
        self.fitness_function = function_name

    def initialize_population(self, pop_size, x_range, y_range):
        population = []
        for i in range(pop_size):
            x = random.choice(x_range)
            y = random.choice(y_range)
            z = self.fitness_function(x, y)
            population.append(np.array([x, y, z]))
        return np.array(population)

    def select_parents(self, parent_array, no_parents):  # truncated rank-based selection
        sorted_dataset = sorted(parent_array, key=lambda output: output[Z])
        return sorted_dataset[0:no_parents]

    def calculate_fitness(self, outputs):
        rank_list = []
        for out in outputs:
            rank_list.append(self.fitness_function(out[0], out[1]))
        return stats.mean(rank_list), stats.stdev(rank_list), rank_list

    # def crossover_function(self, parent_array, offspring_size):
    #     offspring = []
    #     parent_size = len(parent_array)
    #     for i in range(offspring_size):
    #         parent_index = i % parent_size
    #         parent_index2 = i + 1 % parent_size
    #
    #         offspring_x = 0.5 * parent_array[parent_index][X] + parent_array[parent_index2][X]
    #         offspring_y = 0.5 * parent_array[parent_index][Y] + parent_array[parent_index2][Y]
    #         offspring_z = self.fitness_function(offspring_x, offspring_y)
    #         offspring.append([offspring_x, offspring_y, offspring_z])
    #     return offspring

    def crossover_function(self, parent_array, pop_size, mantain):
        offspring = []
        parent_size = len(parent_array)
        offspring_size = pop_size
        offset = 0
        if mantain:
            offspring_size -= parent_size
        for i in range(offspring_size):
            if (i % parent_size) == 0:
                offset += 1
            parent_index = i % parent_size
            parent_index2 = (i+offset) % parent_size
            offspring_x = 0.5 * (parent_array[parent_index][X] + parent_array[parent_index2][X])
            offspring_y = 0.5 * (parent_array[parent_index][Y] + parent_array[parent_index2][Y])
            offspring_z = self.fitness_function(offspring_x, offspring_y)
            offspring.append([offspring_x, offspring_y, offspring_z])
        return offspring

    def mutation_function(self, offspring):
        if random.random() <= self.mutation_prob:
            if random.random() <0.5:
                offspring[0] += self.mutation_prob_step
            else:
                offspring[0] -= self.mutation_prob_step
        # num_mutations = np.uint32(  (self.mutation_prob * offspring_crossover)
        # # Mutation changes a single gene in each offspring randomly.
        #
        # for idx in range(offspring_crossover.shape[0]):
        #     # The random value to be added to the gene.
        #     random_value = np.random.uniform(-1.0, 1.0, 1)
        #     offspring_crossover[idx, mutation_indices] = offspring_crossover[idx, mutation_indices] + random_value

        return offspring

    #
    # def crossover_function(self, parents, offspring_size):
    #
    #     offspring = np.empty(offspring_size)
    #
    #     # The point at which crossover takes place between two parents. Usually, it is at the center.
    #
    #     crossover_point = np.uint32(offspring_size[1] / 2)
    #
    #     for k in range(offspring_size[0]):
    #         # Index of the first parent to mate.
    #         parent1_idx = k % parents.shape[0]
    #
    #         # Index of the second parent to mate.
    #         parent2_idx = (k + 1) % parents.shape[0]
    #
    #         # The new offspring will have its first half of its genes taken from the first parent.
    #         offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
    #
    #         # The new offspring will have its second half of its genes taken from the second parent.
    #         offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    #     return offspring
