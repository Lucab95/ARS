import numpy as np
import random
import statistics as stats

X, Y, Z = 0, 1, 2

class GeneticAlgorithm:

    def __init__(self, function_name, mutation_prob, mutation_prob_step):
        self.fitness_function = function_name
        self.mutation_prob = mutation_prob
        self.mutation_prob_step = mutation_prob_step

    def select_parents(self, parent_array, no_parents):  # truncated rank-based selection
        sorted_dataset = sorted(parent_array, key=lambda output: output[Z])
        return sorted_dataset[0:no_parents]

    def crossover_function(self, parent_array, pop_size, mantain):
        W0, W1 = 0, 1
        offspring = []
        parent_size = len(parent_array)
        offspring_size = pop_size
        offset = 0
        if mantain:
            offspring_size -= parent_size

        for i in range(offspring_size):
            if (i % parent_size) == 0:
                offset += 1
            parent_index_A = i % parent_size
            parent_index_B = (i+offset) % parent_size

            #mix the weigths
            W0_A = parent_array[parent_index_A][W0]
            W1_A = parent_array[parent_index_A][W1]
            W0_B = parent_array[parent_index_B][W0]
            W1_B = parent_array[parent_index_B][W1]
            new_W0 = np.ones((len(W0_A), len(W0_A[0])))
            new_W1 = np.ones((len(W1_A), len(W1_A[0])))

            for i in range(len(W0_A)):
                for j in range(len(W0_A[0])):
                    new_W0[i][j] = 0.5 * (W0_A[i][j] + W0_B[i][j])
                    new_W1[i][j] = 0.5 * (W1_A[i][j] + W1_B[i][j])

            offspring.append([new_W0, new_W1])

        return offspring

    def mutation_function(self, offspring):
        for ofspr in offspring:
            for weight_matrix in ofspr:
                for i in range(len(weight_matrix)):
                    for j in range(len(weight_matrix[0])):
                        weight_matrix[i][j] += np.random.uniform(-self.mutation_prob_step, self.mutation_prob_step)
        return offspring

    def calculate_fitness(self, outputs):
        sorted_outputs = sorted(outputs, key=lambda output: output[Z])
        rank_list = []
        for out in sorted_outputs:
            rank_list.append(out[Z])
        return rank_list[0], stats.mean(rank_list), stats.stdev(rank_list)
