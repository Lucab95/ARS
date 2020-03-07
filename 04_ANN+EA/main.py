import sys
import os
import math
import numpy as np
import pygame
import time
from pygame.locals import KEYDOWN, K_DOWN, K_UP, K_LEFT, K_RIGHT
import robot as rb
import dust as du
import environment as env
import genetic_algorithm as ga
import artificial_neural_network as nna


#######################################################
############### GAME PROPERTIES #######################
SIZE_SCREEN = width, height = 1000, 700
DUST_SIZE = 400
COLOR_SCREEN = 255,255,255
COLOR_ENVIROMENT = 90, 90, 255
MAX_DISTANCE_SENSOR = 40
MAX_VELOCITY = 100
MOTOR_GRIP = MAX_VELOCITY/10
ROBOT_RADIUS = 50
DELTA_T = .03
FPS = 200  # Frames per second
MAP_STEPS = 100

ROBOT_DRIVE = True
#######################################################
#######################################################

#######################################################
################# GA PROPERTIES #######################
FITNESS_FUNCTION = 1  # TODO
MUTATION_PROBABILITY = 0.05
MUTATION_P_STEP = 1.5  # TODO
MANTAIN_PARENTS = True

POPULATION_SIZE = 50
PARENTS_NUMBER = int(POPULATION_SIZE / 5)
GENETIC_EPOCHS = 50

LOAD=False
LOAD_EPOCH = 49

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
collision_flag = False  # Indicator of a collision


pygame.init()  # Initializing library

screen = pygame.display.set_mode(SIZE_SCREEN)  # Initializing screen
FPSCLOCK = pygame.time.Clock()  # Refreshing screen rate

ROBOT_POSITION_FIRST_MAP = [90, 90, math.radians(0)]
WALLS_FIRST_MAP = 	[
					[(30, 30), (970, 30)], [(970, 30), (970, 670)], [(970, 670), (30, 670)], [(30, 670),  (30, 30)], #borders
					[(200, 200), (800, 200)],
					[(200, 500), (800, 500)],
					[(200, 200), (200, 500)],
					[(800, 200), (800, 500)]
					]

ROBOT_POSITION_SECOND_MAP = [200, 610, math.radians(120)]
WALLS_SECOND_MAP = 	[
					[(30, 30), (970, 30)], [(970, 30), (970, 670)], [(970, 670), (30, 670)], [(30, 670), (30, 30)],  # borders
					[(200, 200), (800, 200)],
					[(200, 200), (500, 500)],
					[(800, 200), (500, 500)],
					]

ROBOT_POSITION_THIRD_MAP = [600, 100, math.radians(-90)]
WALLS_THIRD_MAP = 	[
					[(30, 30), (970, 30)], [(970, 30), (970, 670)], [(970, 670), (30, 670)], [(30, 670), (30, 30)],  # borders
					[(200, 200), (800, 200)],
					[(200, 200), (600, 600)],
					[(800, 200), (600, 600)],
					[(200, 200), (800, 200)],
					[(200, 500), (800, 500)],
					[(200, 200), (200, 500)],
					[(800, 200), (800, 500)]
					]

SAVING_DIRECTORY = "Save"
try:
	os.mkdir(SAVING_DIRECTORY)
except OSError:
	print("Creation of the directory %s failed" % SAVING_DIRECTORY)
else:
	print("Successfully created the directory %s " % SAVING_DIRECTORY)


def init_new_map(walls, init_position):
	environment = env.Environment(screen, COLOR_ENVIROMENT, walls)
	robot = rb.Robot(screen, 2 * ROBOT_RADIUS, MAX_VELOCITY, MAX_DISTANCE_SENSOR)
	robot.position = init_position
	return environment, robot


# Saves the model in a txt file
def saveModel(epoch,pop, weights1, weights2,score):
	scores=[]
	name = "gen" + str(epoch) + " " + str(pop)
	np.savetxt(("Save\\" + name + "-w1.txt"), weights1, fmt="%s")
	np.savetxt(("Save\\" + name + "-w2.txt"), weights2, fmt="%s")
	scores.append(score)
	np.savetxt(("Save\\" + name +"-score.txt"),scores,fmt="%s")


# Load a model from a txt file
#TODO definirla quando sarà utile
def loadModel(epoch,pop):
	try:
		name = "gen" + str(epoch) + " " + str(pop)
		w1 = np.loadtxt((("Save\\" + name + "-w1.txt")))
		w2 = np.loadtxt(("Save\\" + name + "-w2.txt"))
	except:
		print("The indicated model doesn't exist!")
		time.sleep(2)
		exit(1)
	return w1, w2

# init environment and robot
environment, robot = init_new_map(WALLS_FIRST_MAP, ROBOT_POSITION_FIRST_MAP)
# drawing the environment and move robot
environment.draw_environment()
robot.robot_moving(environment.walls, DELTA_T)
epoch = 0
if LOAD:
	epoch = LOAD_EPOCH

while epoch < GENETIC_EPOCHS:
	# TODO check ff values and find best parents
	# TODO parents reproduction and new offspring
	for pop_index,current_robot in enumerate(population_array):
		# initialize 3 levels
		maps_list = [WALLS_FIRST_MAP, WALLS_SECOND_MAP, WALLS_THIRD_MAP]
		positions_list = [ROBOT_POSITION_FIRST_MAP, ROBOT_POSITION_SECOND_MAP, ROBOT_POSITION_THIRD_MAP]

		robot_array= []
		#initialize weights for current robot
		if LOAD and LOAD_EPOCH == epoch:
			neuralNetwork.weights_0L, neuralNetwork.weights_1L = loadModel(epoch, pop_index)
		else:
			neuralNetwork.weights_0L = current_robot[0]
			neuralNetwork.weights_1L = current_robot[1]


		#start game for current robot
		for new_map, new_position in zip(maps_list, positions_list):

			#change level and reset dust
			environment, robot = init_new_map(new_map, new_position)
			dust = du.Dust(screen, DUST_SIZE)

			# init game loop
			for steps in range(MAP_STEPS):
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

				if ROBOT_DRIVE:
					# calculate Vl and Vr from [0,1]
					output = neuralNetwork.forward_propagation(robot.sensor_list)
					robot.motor = neuralNetwork.mapping_output_velocity(output, robot.max_velocity)
					#print("SENSORS: ", robot.sensor_list)
					#print("OUTPUTS: ", output)
					#print("VELOCITY: ", robot.motor)

				# Update screen, robot and environment
				screen.fill(COLOR_SCREEN)  # Background screen
				environment.draw_environment()  # Drawing the environment
				robot.robot_moving(environment.walls, DELTA_T)
				dust.update_dust(robot)
				pygame.display.update()
				FPSCLOCK.tick(FPS)
				#time.sleep(0.5)

			score = 0
			dust_array = dust.get_dust()
			for dust in dust_array:
				if dust[1]:
					score += 1
			print(score)
		saveModel(epoch, pop_index, neuralNetwork.weights_0L, neuralNetwork.weights_1L, score)
		pop_index +=1
		epoch +=1
		# TODO save 3 ff values
