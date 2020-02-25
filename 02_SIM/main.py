
import pygame
import sys
import numpy as np
import math
from pygame.locals import K_t, K_g, K_w, K_s, K_o, K_l, K_x, KEYDOWN
import time
import robot as rb

#######################################################
################# PROPERTIES ##########################
SIZE_SCREEN = width, height = 1000, 780
COLOR_SCREEN = 255,255,255
COLOR_ENVIROMENT = 90, 90, 90

MAX_VELOCITY = 100
MOTOR_GRIP = MAX_VELOCITY/10
ROBOT_RADIUS = 40
ROBOT_POSITION = [200, 200, 90] # X Y THETA in GRAD
DELTA_T = .02
FPS = 100 #Frames per second
#######################################################
#######################################################

X, Y, th = 0, 1, 2
L, R = 0, 1
class Environment():
	margin = 30
	def __init__(self, points=[[0+margin,0+margin], [width-margin,0+margin], [width-margin,height-margin], [0+margin,height-margin]]):
		self.points = points

	def draw_environment(self):
		prev = self.points[0]
		rects = []
		for point in self.points:
			rects.append(pygame.draw.line(screen, COLOR_ENVIROMENT, prev, point, 2))
			prev = point
		rects = rects[1:]
		rects.append(pygame.draw.line(screen, COLOR_ENVIROMENT, self.points[-1], self.points[0], 2))
		return rects

	def get_limits(self):
		x_max = max(np.transpose(self.points)[0])
		x_min = min(np.transpose(self.points)[0])
		y_max = max(np.transpose(self.points)[1])
		y_min = min(np.transpose(self.points)[1])
		return x_max, x_min, y_max, y_min


# == MAIN ==
pygame.init()  # Initializing library
screen = pygame.display.set_mode(SIZE_SCREEN)  # Initializing screen
FPSCLOCK = pygame.time.Clock()  # Refreshing screen rate

env = Environment() # Creating the environment
coords_env = env.draw_environment() # Drawing the environment
limits_env = env.get_limits() # Getting the boundaries of the environment

flag_coll = False # Inidcator of a collision

#init robot
robot = rb.Robot(2*ROBOT_RADIUS, MAX_VELOCITY)
robot.position = [ROBOT_POSITION[0], ROBOT_POSITION[1], math.radians(ROBOT_POSITION[2])]
coords_robot = robot.draw_robot(screen, flag_coll) # Placing the robot

# Main loop of the game
while True:
	screen.fill(COLOR_SCREEN) # Background screen

	for event in pygame.event.get():  # Event observer
		if event.type == pygame.QUIT: # Exit
			pygame.quit()
			sys.exit(1)

		##### >>>>> COMPLEX MOVE <<<<< #####
		if event.type == KEYDOWN: # Press key
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

	#Update robot and environment
	coords_env = env.draw_environment() # Drawing the environment
	col_flag = robot.update_position(limits_env, DELTA_T)
	robot.use_sensors(screen, coords_env)
	coords_robot = robot.draw_robot(screen, col_flag) # Placing the robot

	#Update screen
	pygame.display.update()
	FPSCLOCK.tick(FPS)
