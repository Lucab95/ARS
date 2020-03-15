import os
import sys
import pygame
from pygame.locals import KEYDOWN, K_w, K_s, K_d, K_a, K_x
import data as dt
import robot as rb
import dust as du
import environment as env
import genetic_algorithm as ga
import artificial_neural_network as nna
import saving as save
import plotting as plot


X, Y, TH = 0, 1, 2
V, O = 0, 1

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
		####################### N LEVEL FOR 1 ROBOT ##############################################
		#reset level position and dust
		environment = env.Environment(screen, dt.COLOR_WALLS, dt.COLOR_SENSORS)
		environment.maze_environment()

		robot = rb.Robot(screen, 2 * dt.ROBOT_RADIUS, dt.MAX_VELOCITY, dt.MAX_DISTANCE_SENSOR)
		robot.position = dt.ROBOT_POSITION
		robot.use_sensors(environment.walls)

		####################### SINGLE LEVEL ################################################
		for steps in range(dt.MAP_STEPS):
			##################### MANUAL DRIVE ######################################
			for event in pygame.event.get():  # Event observer
				if event.type == pygame.QUIT:  # Exit
					pygame.quit()
					sys.exit(1)
				if event.type == KEYDOWN: # Press key
					if event.key == K_w:
						robot.update_motion(V, dt.MOTION_STEP[V])
					if event.key == K_s:
						robot.update_motion(V, -dt.MOTION_STEP[V])
					if event.key == K_d:
						robot.update_motion(O, dt.MOTION_STEP[O])
					if event.key == K_a:
						robot.update_motion(O, -dt.MOTION_STEP[O])
					if event.key == K_x:
						robot.new_motion(V, 0)
						robot.new_motion(O, 0)

			# Update screen, robot and environment
			screen.fill(dt.COLOR_SCREEN)  # Background screen
			environment.draw_environment()  # Drawing the environment
			collided = robot.robot_moving(environment.walls, dt.DELTA_T)
			pygame.display.update()
			FPSCLOCK.tick(dt.FPS)
