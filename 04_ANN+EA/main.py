import pygame
import sys
import numpy as np
import math
from pygame.locals import K_t, K_g, K_w, K_s, K_o, K_l, K_x, KEYDOWN
import robot as rb
import environment as env
import time

#######################################################
################# PROPERTIES ##########################
SIZE_SCREEN = width, height = 1000, 700
COLOR_SCREEN = 255, 255, 255
COLOR_ENVIROMENT = 90, 90, 255
MAX_DISTANCE_SENSOR = 30
MAX_VELOCITY = 100
MOTOR_GRIP = MAX_VELOCITY/10
ROBOT_RADIUS = 30
DELTA_T = .02
FPS = 200  # Frames per second
MAP_STEPS = 50 #int(DELTA_T * 5000)
#######################################################
#######################################################


# == MAIN ==
L, R = 0, 1
X, Y, TH = 0, 1, 2
collision_flag = False  # Inidcator of a collision
pygame.init()  # Initializing library

screen = pygame.display.set_mode(SIZE_SCREEN)  # Initializing screen
FPSCLOCK = pygame.time.Clock()  # Refreshing screen rate

#GAME_BORDERS = 	[[(30, 30), (970, 30)], [(970, 30), (970, 670)], [(970, 670), (30, 670)], [(30, 670),  (30, 30)]]

ROBOT_POSITION_FIRST_MAP = [100, 100, math.radians(0)]
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
	maps = 	[ WALLS_FIRST_MAP, WALLS_SECOND_MAP, WALLS_THIRD_MAP]
	positions = [ROBOT_POSITION_FIRST_MAP, ROBOT_POSITION_SECOND_MAP, ROBOT_POSITION_THIRD_MAP]
	if steps >= MAP_STEPS:
		if n_map >= 2:# GAME OVER
			pygame.quit()
			sys.exit(1)

		n_map +=1
		steps = 0
		environment, robot = init_new_map(maps[n_map], positions[n_map])
	steps += 1
	return steps, n_map, environment, robot

# init environment and robot
environment, robot = init_new_map(WALLS_FIRST_MAP, ROBOT_POSITION_FIRST_MAP)
# drawing the environment and move robot
environment.draw_environment()
robot.robot_moving(environment.walls, DELTA_T)


# Main loop of the game
current_map ,steps = 0, 0
while True:
	steps, current_map, environment, robot = game_check(steps, current_map, environment, robot)

	for event in pygame.event.get():  # Event observer
		if event.type == pygame.QUIT:  # Exit
			pygame.quit()
			sys.exit(1)

		##### >>>>> COMPLEX MOVE <<<<< #####
		if event.type == KEYDOWN:  # Press key
			if event.key == K_w:
				robot.ChangeMotorVelocity(L,  MOTOR_GRIP)
			if event.key == K_s:
				robot.ChangeMotorVelocity(L, -MOTOR_GRIP)
			if event.key == K_o:
				robot.ChangeMotorVelocity(R,  MOTOR_GRIP)
			if event.key == K_l:
				robot.ChangeMotorVelocity(R, -MOTOR_GRIP)
			if event.key == K_t:
				robot.ChangeMotorVelocity(L,  MOTOR_GRIP)
				robot.ChangeMotorVelocity(R,  MOTOR_GRIP)
			if event.key == K_g:
				robot.ChangeMotorVelocity(L,  -MOTOR_GRIP)
				robot.ChangeMotorVelocity(R,  -MOTOR_GRIP)
			if event.key == K_x:
				robot.NewMotorVelocity(L,  0)
				robot.NewMotorVelocity(R,  0)

	# Update robot and environment
	screen.fill(COLOR_SCREEN)  # Background screen
	environment.draw_environment()  # Drawing the environment
	robot.robot_moving(environment.walls, DELTA_T)

	# Update screen
	pygame.display.update()
	FPSCLOCK.tick(FPS)
