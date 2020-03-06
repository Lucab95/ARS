import pygame
import sys
import numpy as np
import math
from pygame.locals import K_t, K_g, K_w, K_s, K_o, K_l, K_x, KEYDOWN
import robot as rb
import environment as env
import genetic_algorithm as ga
import artificial_neural_network as nna


#######################################################
############### GAME PROPERTIES #######################
SIZE_SCREEN = width, height = 1000, 700
COLOR_SCREEN = 255, 255, 255
COLOR_ENVIROMENT = 90, 90, 255
MAX_DISTANCE_SENSOR = 40
MAX_VELOCITY = 100
MOTOR_GRIP = MAX_VELOCITY/10
ROBOT_RADIUS = 40
DELTA_T = .02
FPS = 200  # Frames per second
MAP_STEPS = 300 #int(DELTA_T * 5000)
#######################################################
#######################################################

#######################################################
################# GA PROPERTIES #######################
FITNESS_FUNCTION = 1  # TODO
POPULATION_SIZE = 3
PARENTS_NUMBER = int(POPULATION_SIZE / 5)
MUTATION_PROBABILITY = 0.05
MUTATION_P_STEP = 1.5  # TODO
MANTAIN_PARENTS = True

GENETIC_EPOCHS = 50
#######################################################
#######################################################

#######################################################
################# NNA PROPERTIES ######################
INPUTS_SIZE = 12
HIDDEN_LAYER_SIZE = 24
OUTPUTS_SIZE = 2

#######################################################
#######################################################

# == INIT NNA, GA AND POPULATION ==
neuralNetwork = nna.ArtificialNeuralNetwork(INPUTS_SIZE, HIDDEN_LAYER_SIZE, OUTPUTS_SIZE)
geneticAlgorithm = ga.GeneticAlgorithm(FITNESS_FUNCTION, MUTATION_PROBABILITY, MUTATION_P_STEP)
FF_results = [[], [], []]  # best, media,stdev
population_array = []
for i in range(POPULATION_SIZE):
	population_array.append(neuralNetwork.initialize_random_weights())

# == INIT GAME ==
L, R = 0, 1
X, Y, TH = 0, 1, 2
collision_flag = False  # Inidcator of a collision
pygame.init()  # Initializing library

screen = pygame.display.set_mode(SIZE_SCREEN)  # Initializing screen
FPSCLOCK = pygame.time.Clock()  # Refreshing screen rate

ROBOT_POSITION_FIRST_MAP = [90, 90, math.radians(0)]
WALLS_FIRST_MAP = 		[
						[(30, 30), (970, 30)],
						[(970, 30), (970, 670)],
						[(970, 670), (30, 670)],
						[(30, 670),  (30, 30)],
						[(200, 200), (800, 200)],
						[(200, 500), (800, 500)],
						[(200, 200), (200, 500)],
						[(800, 200), (800, 500)]
						]

ROBOT_POSITION_SECOND_MAP = [200, 600, math.radians(120)]
WALLS_SECOND_MAP = 		[
						[(30, 30), (970, 30)],
						[(970, 30), (970, 670)],
						[(970, 670), (30, 670)],
						[(30, 670),  (30, 30)],
						[(200, 200), (800, 200)],
						[(200, 200), (500, 500)],
						[(800, 200), (500, 500)],
						]

ROBOT_POSITION_THIRD_MAP = [600, 100, math.radians(-90)]
WALLS_THIRD_MAP = 		[
						[(30, 30), (970, 30)],
						[(970, 30), (970, 670)],
						[(970, 670), (30, 670)],
						[(30, 670),  (30, 30)],
						[(200, 200), (800, 200)],
						[(200, 200), (500, 500)],
						[(800, 200), (500, 500)],
						]


def init_new_map(walls, init_position):
	environment = env.Environment(screen, COLOR_ENVIROMENT, walls)
	robot = rb.Robot(screen, 2 * ROBOT_RADIUS, MAX_VELOCITY, MAX_DISTANCE_SENSOR)
	robot.position = init_position
	return environment, robot

def game_check(steps, n_map, environment, robot):
	maps = [ WALLS_FIRST_MAP, WALLS_SECOND_MAP, WALLS_THIRD_MAP]
	positions = [ROBOT_POSITION_FIRST_MAP, ROBOT_POSITION_SECOND_MAP, ROBOT_POSITION_THIRD_MAP]
	if steps >= MAP_STEPS:
		if n_map >= 2:# GAME OVER
			pygame.quit()
			sys.exit(1)

		n_map += 1
		steps = 0
		environment, robot = init_new_map(maps[n_map], positions[n_map])
	steps += 1
	return steps, n_map, environment, robot


# init environment and robot
environment, robot = init_new_map(WALLS_FIRST_MAP, ROBOT_POSITION_FIRST_MAP)
# drawing the environment and move robot
environment.draw_environment()
robot.robot_moving(environment.walls, DELTA_T)


for epoch in range(GENETIC_EPOCHS):
	# confronta i valori e trova i 10 genitori

	# fai figliare i genitori e crea 50 nuovi robot

	for current_robot in population_array:
		#initialize weights for current robot
		neuralNetwork.weights_0L = current_robot[0]
		neuralNetwork.weights_1L = current_robot[1]

		#start game for current robot
		current_map, steps = 0, 0
		CONTINUE_GAME = True
		# Main loop of the game
		while CONTINUE_GAME:
			steps, current_map, environment, robot = game_check(steps, current_map, environment, robot)

			# calculate Vl and Vr from [0,1]
			output = neuralNetwork.forward_propagation(robot.sensor_list)
			print(output)
			robot.motor = neuralNetwork.mapping_output(output, [[-robot.max_velocity, robot.max_velocity],[-robot.max_velocity, robot.max_velocity]])
			print(robot.motor)
			# mapping Vl and Vr output
			# TODO

			# Update robot and environment
			screen.fill(COLOR_SCREEN)  # Background screen
			environment.draw_environment()  # Drawing the environment
			robot.robot_moving(environment.walls, DELTA_T)

			# Update screen
			pygame.display.update()
			FPSCLOCK.tick(FPS)

		# salva i 3 valori ff ottenuti