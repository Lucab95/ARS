
import pygame
import sys
import numpy as np
import random
from pygame.locals import K_t, K_g, K_w, K_s, K_o, K_l, K_x, K_ESCAPE, KEYDOWN, QUIT
import time
from shapely.geometry import LineString
from shapely.geometry import Point



### PROPERTIES ###

debug = False
FPS = 60 #Frames per second

SIZE_PANEL = 0
SIZE_SCREEN = width, height = 1000+SIZE_PANEL, 780

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


pygame.init() #Initializing library
screen = pygame.display.set_mode(SIZE_SCREEN) # Initializing screen
FPSCLOCK = pygame.time.Clock() #Refreshing screen rate
fontObj = pygame.font.Font("C:/Windows/Fonts/comicbd.ttf", 10) #Font of the messages
fontObj2 = pygame.font.Font("C:/Windows/Fonts/comicbd.ttf", 15) #Font of the messages


		
class Robot():
	def __init__(self, init_pos = [(width-SIZE_PANEL)/2, height/2], length=30, init_direct = 0):
		self.position = np.asarray(init_pos).astype(float)
		self.length = int(length) # The size will affect how the robot behaves (separation between wheels)
		self.direction = init_direct
		self.speed = 0
		self.speed_right = 0
		self.speed_left = 0
		self.rotation = 0
		self.R = 999999999999999999999999999999999999999999999999999999999999999
		self.w = 0
		self.distance_sensors = 200
		#self.sensors = [None]*12
		self.value_sensors = [0]*12



	def use_sensors(self, env):
		angle = self.direction
		#print(env)
		sensors = [None]*12
		for i in range(12):
			# Draw lines
			sensor_x = int(self.position[0] + (self.length) * np.cos(np.radians(angle))) # self.length indicates how long has to be the sensor outside of the circle
			sensor_y = int(self.position[1] + (self.length) * np.sin(np.radians(angle)))
			start_x = int(self.position[0] + (self.distance_sensors+self.length) * np.cos(np.radians(angle)))
			start_y = int(self.position[1]) + (self.distance_sensors+self.length) * np.sin(np.radians(angle))
			sensors[i]=(pygame.draw.line(screen, WHITE, (start_x, start_y), (sensor_x, sensor_y), 1))
			angle +=30
			# Check intersections		
			self.value_sensors[i] = self.distance_sensors #Initializing sensors values
			# Creating the sensor line
			line_sensor = LineString([sensors[i].topleft, sensors[i].bottomright])
			for j in range(len(env)):
				# Creating the environment line
				line_env=LineString([env[j].topleft, env[j].bottomright])
				# If collision -> Take value
				if str(line_sensor.intersection(line_env))!="LINESTRING EMPTY":
					point = Point(self.position)
					self.value_sensors[i] = int(point.distance(line_sensor.intersection(line_env))-self.length)


					




	def draw_robot(self, coll_flag, speeds=[5,5]):
		#Colours for collision
		if coll_flag: colour_robot  = COLLISION_COLOUR
		else: colour_robot = COLOUR_ROBOT
		#Body of the robot
		coord_robot = pygame.draw.circle(screen, colour_robot, (int(self.position[0]), int(self.position[1])), self.length, 2)
		#Head of the robot
		head_x = self.position[0]+(self.length/1.3)*np.cos(np.radians(self.direction))
		head_y = self.position[1]+(self.length/1.3)*np.sin(np.radians(self.direction))
		pygame.draw.line(screen, colour_robot, self.position, [head_x, head_y], 2) 
		#Sensors of the robot		
		angle = self.direction
		for val in self.value_sensors:
			pos_x = self.position[0]+(self.length/0.7)*np.cos(np.radians(angle))
			pos_y = self.position[1]+(self.length/0.7)*np.sin(np.radians(angle))
			textSurfaceObj = fontObj.render(str(val), True, COLOUR_FONT, WHITE) # 
			textRectObj = textSurfaceObj.get_rect()                             #
			textRectObj.center = (pos_x, pos_y)
			screen.blit(textSurfaceObj, textRectObj)                           
			angle +=30
		#Velocities of the motors
		pos_x = self.position[0]+(self.length/2)*np.cos(np.radians(self.direction-90))
		pos_y = self.position[1]+(self.length/2)*np.sin(np.radians(self.direction-90))
		textSurfaceObj = fontObj2.render(str(self.speed_left), True, COLOUR_FONT, WHITE) # Left motor
		textRectObj = textSurfaceObj.get_rect()                            #
		textRectObj.center = (pos_x, pos_y)                                #
		screen.blit(textSurfaceObj, textRectObj)                           #
		pos_x = self.position[0]+(self.length/2)*np.cos(np.radians(self.direction+90))
		pos_y = self.position[1]+(self.length/2)*np.sin(np.radians(self.direction+90))
		textSurfaceObj = fontObj2.render(str(self.speed_right), True, COLOUR_FONT, WHITE) # Right motor
		textRectObj = textSurfaceObj.get_rect()                            #
		textRectObj.center = (pos_x, pos_y)                                #
		screen.blit(textSurfaceObj, textRectObj)                           #

		if debug:
			print("\n>>Speed:", self.speed, " (Right:", self.speed_right,", Left:", self.speed_left, ")")
			print(">>Rotation: ", self.rotation)
			print(">>Direction:", self.direction)
		return coord_robot


	def move_robot(self, sp, rot):
		#Change speed
		self.speed +=sp
		# Change rotation
		self.rotation += rot
		self.draw_robot()


	def update_pos(self, limits_env):
		marg = 1
		# Updating direction
		self.direction =  self.direction+self.rotation
		if self.direction < 0: self.direction = 359   # Limits in 
		elif self.direction > 359: self.direction = 0 # the angtles
		# Updating position
		inc_x = self.speed*np.cos(np.radians(self.direction))
		inc_y = self.speed*np.sin(np.radians(self.direction))
		new_x = (self.position[0]+inc_x)
		new_y = (self.position[1]+inc_y)
		# COLLISION DETECTION
		# Checking limits environment
		if self.position[0]+self.length >= limits_env[0]: # Right boundary
			new_x = limits_env[0]-self.length-marg
			print("Collision at time",time.time(),"in the position",self.position)
		elif self.position[0]-self.length <= limits_env[1]: # Left boundary
			new_x = limits_env[1]+self.length+marg
			print("Collision at time",time.time(),"in the position",self.position)
		if self.position[1]+self.length >= limits_env[2]: # Up boundary
			new_y = limits_env[2]-self.length-marg
			print("Collision at time",time.time(),"in the position",self.position)
		elif self.position[1]-self.length <= limits_env[3]: # Down boundary
			new_y = limits_env[3]+self.length+marg
			print("Collision at time",time.time(),"in the position",self.position)
		#Updating position
		self.position = [new_x, new_y]



	def move_robot_complex(self, inc_right, inc_left):
		#Change velocity wheels
		self.speed_right += inc_right
		self.speed_left += inc_left
		#Change speed
		self.speed = (self.speed_right + self.speed_left)/2
		# Calculating R (Point of Rotation)
		try: # If both speeds are zero -> R = 0 (Error when diving by 0)
			self.R = (self.length/2)*((self.speed_left+self.speed_right)/(self.speed_right-self.speed_left))
		except:
			#self.R = np.inf	
			self.R = 999999999999999999999999999999999999999999999999999999999999999
		# Calculating w (Rate Rotation or Rotation Angle)
		self.w = (self.speed_right-self.speed_left)/self.length #TODO probabilmente era questo che dava problemi perchè usava la lunghexza invece del raggio




	def update_pos_complex(self, limits_env):
		# Timesteps
		param = 2
		# Collission flag
		coll_flag = False
		# Calculating new X, Y & Orientation
		if self.speed_right!=self.speed_left:
			# Calculating ICC
			ICC_x = self.position[0]-self.R*np.sin(np.radians(self.direction))
			ICC_y = self.position[1]-self.R*np.cos(np.radians(self.direction))
			# Matrixes involved
			rot_mat = np.asarray([[np.cos(self.w*param), -np.sin(self.w*param), 0],
								[np.sin(self.w*param), np.cos(self.w*param), 0],
								[0, 0, 1]])  
			second_mat = [self.position[0]-ICC_x, self.position[1]-ICC_y, np.radians(self.direction)]
			third_mat = [ICC_x, ICC_y, self.w*param]
			# New coordinates and orientation
			new_x, new_y, new_dir = np.dot(rot_mat, second_mat)+third_mat
			self.direction =  np.degrees(new_dir)
		else:
 			# Updating position
			inc_x = self.speed*np.cos(np.radians(self.direction))
			inc_y = self.speed*np.sin(np.radians(self.direction))
			new_x = (self.position[0]+inc_x)
			new_y = (self.position[1]+inc_y)

 		#Margin
		marg = 1
		#Limits of the angles
		if self.direction < 0: self.direction = 359   # Limits in 
		elif self.direction > 359: self.direction = 0 # the angles

		# COLLISION DETECTION
		# Checking limits environment
		if self.position[0]+self.length >= limits_env[0]: # Right boundary
			new_x = limits_env[0]-self.length-marg
			coll_flag = True
			print("Collision at time",time.time(),"in the position",self.position)
		elif self.position[0]-self.length <= limits_env[1]: # Left boundary
			new_x = limits_env[1]+self.length+marg
			coll_flag = True
			print("Collision at time",time.time(),"in the position",self.position)
		if self.position[1]+self.length >= limits_env[2]: # Up boundary
			new_y = limits_env[2]-self.length-marg
			coll_flag = True
			print("Collision at time",time.time(),"in the position",self.position)
		elif self.position[1]-self.length <= limits_env[3]: # Down boundary
			new_y = limits_env[3]+self.length+marg
			coll_flag = True
			print("Collision at time",time.time(),"in the position",self.position)

		self.position = [new_x, new_y]
		return coll_flag



	def stop_robot(self):
		self.speed_right = 0
		self.speed_left = 0
		self.speed = 0





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





def main():

	env = Environment() # Creating the environment
	coords_env = env.draw_env() # Drawing the environment
	limits_env = env.get_limits() # Getting the boundaries of the environment

	robot = Robot(length=30) # Creating the robot
	coords_robot = robot.draw_robot(False) # Placing the robot
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





if __name__ == '__main__':
    main()
