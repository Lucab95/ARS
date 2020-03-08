import sys
import math
import pygame
from pygame.locals import KEYDOWN, K_DOWN, K_UP, K_LEFT, K_RIGHT
from copy import deepcopy
import robot as rb
import dust as du
import environment as env
import genetic_algorithm as ga
import artificial_neural_network as nna
import saving as save
L, R = 0, 1
X, Y, TH = 0, 1, 2

#######################################################
############### GAME PROPERTIES #######################
SIZE_SCREEN = width, height = 1000, 700
DUST_SIZE = 400
COLOR_SCREEN = 255,255,255
COLOR_ENVIROMENT = 90, 90, 255
MAX_DISTANCE_SENSOR = 50
MAX_VELOCITY = 100
MOTOR_GRIP = MAX_VELOCITY/10
ROBOT_RADIUS = 50
DELTA_T = .15
FPS = 200  # Frames per second
MAP_STEPS = 15

ROBOT_DRIVE = True
#######################################################
#######################################################

#######################################################
################# GA PROPERTIES #######################
FITNESS_FUNCTION = 1  # TODO
MUTATION_PROBABILITY = 0.05
MUTATION_P_STEP = 1.5
MANTAIN_PARENTS = True

POPULATION_SIZE = 15
PARENTS_NUMBER = int(POPULATION_SIZE / 5)
GENETIC_EPOCHS = 50

LOAD = False
LOAD_EPOCH = 49

SCORE_INCIDENCE = 0.6
AVOID_COLLISIONS_INCIDENCE = 1-SCORE_INCIDENCE
#######################################################
#######################################################

#######################################################
################# NNA PROPERTIES ######################
INPUTS_SIZE = 13
HIDDEN_LAYER_SIZE = int(2*INPUTS_SIZE)
OUTPUTS_SIZE = 2
#######################################################
#######################################################

#######################################################
############### OTHER PROPERTIES ######################
SAVING_DIRECTORY, SCORE_DIRECTORY = "Save", "Score"

ROBOT_POSITION_FIRST_MAP = [90, 90, math.radians(0)]
WALLS_FIRST_MAP = 	[
					[(10,10),(990,10)],
					[(10,10),(10,690)],
					[(990,690),(10,690)],
					[(990,690),(990,10)]
					]

ROBOT_POSITION_SECOND_MAP = [900, 380, math.radians(120)]
WALLS_SECOND_MAP = 	[
					[(10,10),(990,110)],   # borders
					[(10,10),(10,690)],
					[(990,590),(10,690)],
					[(990,590),(990,110)],
					[(210,210),(790,310)],   # inside
					[(210,210),(210,490)],
					[(790,390),(210,490)],
					[(790,390),(790,310)],
					]
#######################################################
#######################################################

save.create_directory(SAVING_DIRECTORY)
save.create_directory(SCORE_DIRECTORY)

# == INIT GAME ==
pygame.init()  # Initializing library
screen = pygame.display.set_mode(SIZE_SCREEN)  # Initializing screen
FPSCLOCK = pygame.time.Clock()  # Refreshing screen rate

# == INIT NNA, GA AND POPULATION ==
neuralNetwork = nna.ArtificialNeuralNetwork(INPUTS_SIZE, HIDDEN_LAYER_SIZE, OUTPUTS_SIZE)
geneticAlgorithm = ga.GeneticAlgorithm(FITNESS_FUNCTION, MUTATION_PROBABILITY, MUTATION_P_STEP)

population_array = []
for i in range(POPULATION_SIZE):
	population_array.append(neuralNetwork.initialize_random_weights())


def init_new_map(walls, init_position):
	environment = env.Environment(screen, COLOR_ENVIROMENT, walls)
	robot = rb.Robot(screen, 2 * ROBOT_RADIUS, MAX_VELOCITY, MAX_DISTANCE_SENSOR)
	robot.position = init_position
	return environment, robot


maps_list = [WALLS_FIRST_MAP, WALLS_SECOND_MAP]
positions_list = [ROBOT_POSITION_FIRST_MAP, ROBOT_POSITION_SECOND_MAP]
collision_flag = False  # Indicator of a collision
epoch = 1
if LOAD:  epoch = LOAD_EPOCH

while epoch <= GENETIC_EPOCHS:
	collision_array = [] # collisions[robot][collision_level_1lvl]
	score_array = [] # score[robot][dust_1lvl]
	print("epoch: ", epoch)

	####################### ALL POPULATION FOR 1 EPOCH #############################################
	for pop_index, current_robot in enumerate(population_array):
		#set title with number of epoch and robot
		pygame.display.set_caption("Epoch: " + str(epoch) + "  Robot: " + str(pop_index))

		collision_robot_3lvl = []  # save collision for the single robot for all levels
		score_robot_3lvl = []  # save score for the single robot but for all levels

		#initialize weights for current robot or load them
		if LOAD and LOAD_EPOCH == epoch:
			neuralNetwork.weights_0L, neuralNetwork.weights_1L = save.load_model(epoch, pop_index)
		else:
			neuralNetwork.weights_0L = current_robot[0]
			neuralNetwork.weights_1L = current_robot[1]
			save.save_model_weight(epoch, pop_index, neuralNetwork.weights_0L, neuralNetwork.weights_1L)

		####################### N LEVEL FOR 1 ROBOT ##############################################
		for new_map, new_position in zip(maps_list, positions_list):
			#reset level position and dust
			environment, robot = init_new_map(new_map, new_position)
			dust = du.Dust(screen, DUST_SIZE)
			collision_avoided = 0
			####################### SINGLE LEVEL ################################################
			for steps in range(MAP_STEPS):
				##################### MANUAL DRIVE ######################################
				for event in pygame.event.get():  # Event observer
					if event.type == pygame.QUIT:  # Exit
						pygame.quit()
						sys.exit(1)

					if ROBOT_DRIVE == False:
						if event.type == KEYDOWN: # Press key
							if event.key == K_DOWN:
								robot.ChangeMotorVelocity(L, -MOTOR_GRIP)
								robot.ChangeMotorVelocity(R, -MOTOR_GRIP)
							if event.key == K_UP:
								robot.ChangeMotorVelocity(L, MOTOR_GRIP)
								robot.ChangeMotorVelocity(R, MOTOR_GRIP)
							if event.key == K_LEFT:
								robot.ChangeMotorVelocity(L, -MOTOR_GRIP)
								robot.ChangeMotorVelocity(R, 2*MOTOR_GRIP)
							if event.key == K_RIGHT:
								robot.ChangeMotorVelocity(L, 2*MOTOR_GRIP)
								robot.ChangeMotorVelocity(R, -MOTOR_GRIP)
				#########################################################################

				##################### ROBOT DRIVE #######################################
				if ROBOT_DRIVE:
					# calculate Vl and Vr from [0,1]
					inputs = deepcopy(robot.sensor_list)
					inputs.append(DELTA_T*1000) #delta time in ms
					output = neuralNetwork.forward_propagation(inputs)
					robot.motor = neuralNetwork.mapping_output_velocity(output, robot.max_velocity)
				#########################################################################

				# Update screen, robot and environment
				screen.fill(COLOR_SCREEN)  # Background screen
				environment.draw_environment()  # Drawing the environment
				collided = robot.robot_moving(environment.walls, DELTA_T)
				dust.update_dust(robot)
				pygame.display.update()
				FPSCLOCK.tick(FPS)

				if not collided:
					collision_avoided += 1
			#####################################################################################
			collision_robot_3lvl.append(collision_avoided)
			score = dust.get_score_dust()
			score_robot_3lvl.append(score)
			print(score)
		#########################################################################################
		score_array.append(score_robot_3lvl)
		collision_array.append(collision_robot_3lvl)
	################################################################################################

	#get averages of score and collisions avoided
	average_score = geneticAlgorithm.get_average_value(score_array)
	average_collision_avoided = geneticAlgorithm.get_average_value(collision_array)

	#normalize previous values
	normalized_average_score = geneticAlgorithm.get_normalized_value(average_score, DUST_SIZE)
	normalized_average_collision_avoided = geneticAlgorithm.get_normalized_value(average_collision_avoided, MAP_STEPS)

	fitness_values = geneticAlgorithm.calculate_fitness(SCORE_INCIDENCE, AVOID_COLLISIONS_INCIDENCE, normalized_average_score, normalized_average_collision_avoided)

	# save in a file
	save.save_model_score(epoch, POPULATION_SIZE, score_array, collision_array, average_score, average_collision_avoided, normalized_average_score, normalized_average_collision_avoided, fitness_values)

	# TODO parents reproduction and new offspring
	parents, ordered_fitness = geneticAlgorithm.select_parents(PARENTS_NUMBER, population_array, fitness_values)
	population_array = geneticAlgorithm.crossover_function(population_array, POPULATION_SIZE, MANTAIN_PARENTS)
	population_array = geneticAlgorithm.mutation_function(population_array)

	epoch += 1

# TODO draw all