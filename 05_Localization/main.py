import os
import sys
import pygame
from pygame.locals import KEYDOWN, K_DOWN, K_UP, K_LEFT, K_RIGHT
from copy import deepcopy
import statistics as stats
import data as dt
import robot as rb
import dust as du
import environment as env
import genetic_algorithm as ga
import artificial_neural_network as nna
import saving as save
import plotting as plot


X, Y, TH = 0, 1, 2
L, R = 0, 1

save.create_directory(dt.SAVING_DIRECTORY)
save.create_directory(dt.SCORE_DIRECTORY)
save.create_directory(dt.IMAGES_DIRECTORY)
save.create_directory(dt.BEST_DIRECTORY)

# == INIT GAME ==
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)
pygame.init()  # Initializing library
screen = pygame.display.set_mode(dt.SIZE_SCREEN)  # Initializing screen
FPSCLOCK = pygame.time.Clock()  # Refreshing screen rate

# == INIT NNA, GA AND POPULATION ==
neuralNetwork = nna.ArtificialNeuralNetwork(dt.INPUTS_SIZE, dt.HIDDEN_LAYER_SIZE, dt.OUTPUTS_SIZE)
geneticAlgorithm = ga.GeneticAlgorithm(dt.CROSSOVER_PROBABILITY, dt.MUTATION_PROBABILITY, dt.MUTATION_P_STEP)
performance_FF = [[],[],[]] # best, mean, stdev
population_array = [neuralNetwork.initialize_random_weights() for i in range(dt.POPULATION_SIZE)] # init random parents
collision_flag = False  # Indicator of a collision
epoch = dt.LOAD_EPOCH if dt.LOAD else 0

while epoch <= dt.GENETIC_EPOCHS:
	collision_array = [] # collisions[robot][collision_level_1lvl]
	score_array = [] # score[robot][dust_1lvl]

	####################### ALL POPULATION FOR 1 EPOCH #############################################
	for pop_index, current_robot in enumerate(population_array):
		#set title with number of epoch and robot
		pygame.display.set_caption("Epoch: " + str(epoch) + "  Robot: " + str(pop_index))

		collision_robot_3lvl = []  # save collision for the single robot for all levels
		score_robot_3lvl = []  # save score for the single robot but for all levels

		#initialize weights for current robot or load them
		if dt.LOAD and dt.LOAD_EPOCH == epoch:
			neuralNetwork.weights_0L, neuralNetwork.weights_1L = save.load_model(epoch, pop_index)
		else:
			neuralNetwork.weights_0L = deepcopy(current_robot[0])
			neuralNetwork.weights_1L = deepcopy(current_robot[1])
			save.save_model_weight(epoch, pop_index, neuralNetwork.weights_0L, neuralNetwork.weights_1L)

		####################### N LEVEL FOR 1 ROBOT ##############################################

		#reset level position and dust
		environment = env.Environment(screen, dt.COLOR_WALLS, dt.COLOR_SENSORS)
		environment.maze_environment()

		robot = rb.Robot(screen, 2 * dt.ROBOT_RADIUS, dt.MAX_VELOCITY, dt.MAX_DISTANCE_SENSOR)
		robot.position = dt.ROBOT_POSITION
		robot.use_sensors(environment.walls)

		dust = du.Dust(screen, dt.DUST_SIZE)
		collision_avoided = 0
		####################### SINGLE LEVEL ################################################
		for steps in range(dt.MAP_STEPS):
			##################### MANUAL DRIVE ######################################
			for event in pygame.event.get():  # Event observer
				if event.type == pygame.QUIT:  # Exit
					pygame.quit()
					sys.exit(1)

				if dt.ROBOT_DRIVE == False:
					if event.type == KEYDOWN: # Press key
						if event.key == K_DOWN:
							robot.ChangeMotorVelocity(L, -dt.MOTOR_GRIP)
							robot.ChangeMotorVelocity(R, -dt.MOTOR_GRIP)
						if event.key == K_UP:
							robot.ChangeMotorVelocity(L, dt.MOTOR_GRIP)
							robot.ChangeMotorVelocity(R, dt.MOTOR_GRIP)
						if event.key == K_LEFT:
							robot.ChangeMotorVelocity(L, -dt.MOTOR_GRIP)
							robot.ChangeMotorVelocity(R, 2*dt.MOTOR_GRIP)
						if event.key == K_RIGHT:
							robot.ChangeMotorVelocity(L, 2*dt.MOTOR_GRIP)
							robot.ChangeMotorVelocity(R, -dt.MOTOR_GRIP)
			#########################################################################

			##################### ROBOT DRIVE #######################################
			if dt.ROBOT_DRIVE:
				# calculate Vl and Vr from [0,1]
				inputs = deepcopy(robot.sensor_list)
				inputs.append(dt.DELTA_T*1000) #delta time in ms
				output = neuralNetwork.forward_propagation(inputs)
				robot.motor = neuralNetwork.mapping_output_velocity(output, robot.max_velocity)
			#########################################################################

			# Update screen, robot and environment
			screen.fill(dt.COLOR_SCREEN)  # Background screen
			environment.draw_environment()  # Drawing the environment
			collided = robot.robot_moving(environment.walls, dt.DELTA_T)
			dust.update_dust(robot)
			pygame.display.update()
			FPSCLOCK.tick(dt.FPS)

			if not collided:
				collision_avoided += 1
		#####################################################################################
		collision_robot_3lvl.append(collision_avoided)
		score = dust.get_score_dust()
		score_robot_3lvl.append(score)
		#########################################################################################
		score_array.append(score_robot_3lvl)
		collision_array.append(collision_robot_3lvl)
	################################################################################################

	#get averages of score and collisions avoided
	average_score = geneticAlgorithm.get_average_value(score_array)
	average_collision_avoided = geneticAlgorithm.get_average_value(collision_array)

	#normalize previous values
	normalized_average_score = geneticAlgorithm.get_normalized_value(average_score, dt.DUST_SIZE)
	normalized_average_collision_avoided = geneticAlgorithm.get_normalized_value(average_collision_avoided, dt.MAP_STEPS)
	# get fitness values
	fitness_values = geneticAlgorithm.calculate_fitness(dt.SCORE_INCIDENCE, dt.AVOID_COLLISIONS_INCIDENCE, normalized_average_score, normalized_average_collision_avoided)

	# save in a file
	save.save_model_score(epoch, dt.POPULATION_SIZE, score_array, collision_array, average_score, average_collision_avoided, normalized_average_score, normalized_average_collision_avoided, fitness_values)

	# order stuff
	population_array, fitness_values = geneticAlgorithm.order_population_and_fitness(population_array, fitness_values)

	performance_FF[0].append(fitness_values[0])
	performance_FF[1].append(stats.mean(fitness_values))
	performance_FF[2].append(stats.stdev(fitness_values))
	if epoch == 1 or epoch== 10 or epoch == 50:
		save.save_model_weight_training(epoch, population_array[0][0],population_array[0][1])
	parents = geneticAlgorithm.select_parents(dt.PARENTS_NUMBER, population_array)
	crossover_array = geneticAlgorithm.crossover_function(parents, dt.POPULATION_SIZE, dt.MANTAIN_PARENTS)
	mutated_array = geneticAlgorithm.mutation_function(crossover_array)
	if dt.MANTAIN_PARENTS:
		all_individuals = parents + mutated_array
		population_array = deepcopy(all_individuals)
	else:
		population_array = deepcopy(mutated_array)

	epoch += 1

# write down best, mean, stdev
plot.plotting_performance(performance_FF)