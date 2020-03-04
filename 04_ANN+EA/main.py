import pygame
import sys
import numpy as np
import math
from pygame.locals import K_t, K_g, K_w, K_s, K_o, K_l, K_x, KEYDOWN
import robot as rb
import environment as env

#######################################################
################# PROPERTIES ##########################
SIZE_SCREEN = width, height = 1000, 700
COLOR_SCREEN = 255, 255, 255
COLOR_ENVIROMENT = 90, 90, 255
MAX_DISTANCE_SENSOR = 100
MAX_VELOCITY = 100
MOTOR_GRIP = MAX_VELOCITY/10
ROBOT_RADIUS = 30
ROBOT_POSITION = [200, 300, 60]  # X Y THETA in GRAD
DELTA_T = .03
FPS = 200  # Frames per second
#######################################################
#######################################################


# == MAIN ==
L, R = 0, 1
X, Y, TH = 0, 1, 2
collision_flag = False  # Inidcator of a collision
pygame.init()  # Initializing library

screen = pygame.display.set_mode(SIZE_SCREEN)  # Initializing screen
FPSCLOCK = pygame.time.Clock()  # Refreshing screen rate

#init environment
environment = env.Environment(
	screen,
	COLOR_ENVIROMENT,
	[
		[(30, 30), (970, 30)],
		[(970, 30), (970, 670)],
		[(970, 670), (30, 670)],
		[(30, 670),  (30, 30)],
		[(200, 200), (800, 200)],
		[(200, 200), (500, 500)],
		[(800, 200), (500, 500)],
	]
)
environment.draw_environment()  # drawing the environment

# init robot
robot = rb.Robot(screen, 2*ROBOT_RADIUS, MAX_VELOCITY, MAX_DISTANCE_SENSOR)
robot.position = [ROBOT_POSITION[X], ROBOT_POSITION[Y], math.radians(ROBOT_POSITION[TH])]
robot.robot_moving(environment.walls, DELTA_T)

# Main loop of the game
while True:
	screen.fill(COLOR_SCREEN)  # Background screen

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
	environment.draw_environment()  # Drawing the environment
	robot.robot_moving(environment.walls, DELTA_T)

	# Update screen
	pygame.display.update()
	FPSCLOCK.tick(FPS)
