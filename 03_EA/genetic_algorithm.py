import numpy as np
import random
import statistics as stats

class GeneticAlgorithm:

    def __init__(self, function_name, crossover_prob, crossover_prob_step, mutation_prob, mutation_prob_step):
        self.crossover_prob = crossover_prob
        self.crossover_prob_step = crossover_prob_step
        self.mutation_prob = mutation_prob
        self.mutation_prob_step = mutation_prob_step
        self.fitness_function = function_name

    def initialize_population(self, x, y): #truncated rank-based selection
        population = []
        for i in range(self.pop_size):
            population.append(np.array([random.choice(x), random.choice(y)]))
        return np.array(population)

    def select_parents(self, parents, no_parents):
        rank_list = np.empty(no_parents)
        for i, parent in parents:
            rank_list[i] = (self.fitness_function(parent[0], parent[1]))
        rank_list =np.sort(rank_list)
        reversed = rank_list[::-1]
        print(reversed)
        return reversed[0:no_parents]



    def calculate_fitness(self, outputs):
        rank_list = []
        for out in outputs:
            rank_list.append(self.fitness_function(out[0], out[1]))
        return stats.mean(rank_list), stats.stdev(rank_list), rank_list

    def crossover_function(self, parents, offspring_size):
        offspring = []

        for i, son in offspring_size:
            parent_index = i % len(parents)
            parent_index2= i+1 % len(parents)
            print(len(parents))
            offspring_x = parents[parent_index][0] + parents[parent_index2][0]
            offspring_y = parents[parent_index][1] + parents[parent_index2][1]
            offspring.append([offspring_x,offspring_y])
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

    def mutation_function(self, offspring_crossover, mutation_percent):

        num_mutations = np.uint32((self.mutation_prob * offspring_crossover.shape[1]) / 100) #TODO too much probably
        mutation_indices = np.array(random.sample(range(0, offspring_crossover.shape[1]), num_mutations))

        # Mutation changes a single gene in each offspring randomly.

        for idx in range(offspring_crossover.shape[0]):
            # The random value to be added to the gene.
            random_value = np.random.uniform(-1.0, 1.0, 1)
            offspring_crossover[idx, mutation_indices] = offspring_crossover[idx, mutation_indices] + random_value

        return offspring_crossover



