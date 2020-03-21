import os
import sys
import pygame
from pygame.locals import KEYDOWN, K_w, K_s, K_d, K_a, K_x
import data as dt
import robot as rb
import environment as env

X, Y, TH = 0, 1, 2
V, O = 0, 1

# == INIT GAME ==
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)
pygame.init()  # Initializing library
screen = pygame.display.set_mode(dt.SIZE_SCREEN)  # Initializing screen
FPSCLOCK = pygame.time.Clock()  # Refreshing screen rate

# reset level and position
real_path = []
environment = env.Environment(screen, dt.COLOR_WALLS, dt.COLOR_BEACONS)
environment.maze_environment()

robot = rb.Robot(screen, 2 * dt.ROBOT_RADIUS, dt.MAX_VELOCITY, dt.MAX_DISTANCE_SENSOR)
robot.position = dt.ROBOT_POSITION
robot.use_sensors(environment.walls)
real_path.append(robot.position)

while True:
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
	screen.fill(dt.COLOR_SCREEN)  # reupdate screen
	environment.draw_environment()  # Drawing the environment
	collided = robot.robot_moving(environment.walls, dt.DELTA_T)
	real_path.append(robot.position)
	robot.draw_path(real_path)
	robot.draw_landmarks(environment.walls, environment.beacons)
	pygame.display.update()
	FPSCLOCK.tick(200) #FPS
