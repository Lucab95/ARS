
import pygame
import sys
import numpy as np
from pygame.locals import K_t, K_g, K_w, K_s, K_o, K_l, K_x, KEYDOWN
import time
from shapely.geometry import LineString
from shapely.geometry import Point
import robot as rb


### PROPERTIES ###

DEBUG = False
FPS = 100 #Frames per second

SIZE_PANEL = 0
SIZE_SCREEN = width, height = 1000 + SIZE_PANEL, 780

#Colours
WHITE = 255,255,255
BLACK = 0, 0, 0
GREEN = 0,255,0
RED = 255,0,0
BLUE = 0,0,255
GREY = 90,90,90
LIGHT_GREY = 150,150,150

COLOUR_ROBOT = GREY
COLOUR_CONT = BLACK
COLOUR_FONT = LIGHT_GREY
COLLISION_COLOUR = RED

#######################################################
################# VARIABLES ###########################
SCREEN_SIZE_X = 900
SCREEN_SIZE_Y = 700
SCREEN_COLOR = (0, 0, 0)
ROBOT_COLOR = (255, 255, 0)
WALL_COLOR = (33, 33, 222)

MAX_VELOCITY = 1000
ROBOT_RADIUS = 50
ROBOT_POSITION = [200, 200]
ROBOT_ORIENTATION =  45 # IN GRAD
DELTA_T = .02
SLEEP_MILLIS = 100
MOTOR_GRIP = MAX_VELOCITY/10
#######################################################
#######################################################

X, Y, th = 0, 1, 2

class Environment():
	margin = 30
	def __init__(self, points=[[0+margin,0+margin], [width-margin-SIZE_PANEL,0+margin], [width-margin-SIZE_PANEL,height-margin], [0+margin,height-margin]]):
		self.points = points

	def draw_env(self):
		# return pygame.draw.polygon(screen, COLOUR_ROBOT, self.points, 2)
		prev = self.points[0]
		rects = []
		for point in self.points:
			rects.append(pygame.draw.line(screen, COLOUR_ROBOT, prev, point, 2))
			prev = point
		rects = rects[1:]
		rects.append(pygame.draw.line(screen, COLOUR_ROBOT, self.points[-1], self.points[0], 2))		
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
fontObj = pygame.font.Font("C:/Windows/Fonts/comicbd.ttf", 10)  # Font of the messages
fontObj2 = pygame.font.Font("C:/Windows/Fonts/comicbd.ttf", 15)  # Font of the messages

env = Environment() # Creating the environment
coords_env = env.draw_env() # Drawing the environment
limits_env = env.get_limits() # Getting the boundaries of the environment

#init robot
robot = rb.Robot(2*ROBOT_RADIUS, MAX_VELOCITY)
theta = np.radians(ROBOT_ORIENTATION)
robotPosition = [ROBOT_POSITION[0], ROBOT_POSITION[1], theta] # X, Y, theta

coords_robot = draw_robot(robotPosition, False) # Placing the robot

flag_coll = False # Inidcator of a collision

# Main loop of the game
while True:
	screen.fill(WHITE) # Background screen
	for event in pygame.event.get():  # Event observer
		if event.type == pygame.QUIT: # Exit
			pygame.quit()
			sys.exit(1)

		##### >>>>> SIMPLE MOVE <<<<< #####

		# if event.type == KEYDOWN: # Press key
		# 	inc_sp = 0
		# 	inc_rot = 0
		# 	if event.key == K_t: inc_sp = +1
		# 	elif event.key == K_g: inc_sp = -1
		# 	elif event.key == K_x: robot.stop_robot()
		# 	elif event.key == K_w: inc_rot = +1
		# 	elif event.key == K_s: inc_rot = -1
		# 	robot.move_robot(inc_sp, inc_rot)


		##### >>>>> COMPLEX MOVE <<<<< #####
		if event.type == KEYDOWN: # Press key
			inc_right = 0
			inc_left = 0
			if event.key == K_w: inc_left = +1
			if event.key == K_s: inc_left = -1
			if event.key == K_o: inc_right = +1
			if event.key == K_l: inc_right = -1
			if event.key == K_x: robot.stop_robot()
			if event.key == K_t: inc_left = inc_right = +1
			if event.key == K_g: inc_left = inc_right = -1
			robot.move_robot_complex(inc_right, inc_left)

	#Update robot and environment
	coords_env = env.draw_env() # Drawing the environment
	#robot.update_pos(limits_env)
	col_flag = robot.update_pos_complex(limits_env)
	robot.use_sensors(coords_env)
	coords_robot = robot.draw_robot(col_flag) # Placing the robot


	#Update screen
	pygame.display.update()
	FPSCLOCK.tick(FPS)


