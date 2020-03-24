# -*- coding: utf-8 -*-
"""
@author: Glauco
"""
from copy import deepcopy
import math
import pygame
import numpy as np
import shapely
from shapely.geometry import LineString, Point
from shapely import affinity
import data as dt
import localization

L, R = 0, 1
X, Y, TH = 0, 1, 2
V, O = 0, 1
inf_number = math.pow(10, 50)

class Robot():
  def __init__(self, screen, length, max_velocity, max_distance_sensor):
    self.screen = screen
    self.color = [90, 90, 90]
    self.position = [0, 0, 0]  # X Y THradians
    self.axis_length = length
    self.max_velocity = max_velocity
    self.motion = [0, 0] # V, O
    self.max_distance_sensor = max_distance_sensor
    self.localization = localization.Localization(self.motion)

  def round(self, value):
    return int(round(value))

  def round_Y(self, value):  # INVERT Y to get a right movement and axis origin
    return int(round(self.screen.get_size()[Y] - value))

  def round_point(self, point):  # INVERT Y to get a right movement and axis origin
    return (self.round(point[X]), self.round(self.screen.get_size()[Y] - point[Y]))

  def set_in_range(self, limit, value): # force value to stay in a range[min, max]
    if value > limit:
      value = limit
    elif value < -limit:
      value = -limit
    return value

  def new_motion(self, n_motion, value):
    self.motion[n_motion] = self.set_in_range(self.max_velocity[n_motion], value)

  def update_motion(self, n_motion, value):
    next_value = self.motion[n_motion] + value
    self.motion[n_motion] = self.set_in_range(self.max_velocity[n_motion], next_value)

  def simplified_kinematics(self, position, dT):
    next_position = deepcopy(position)  # X' Y' th'
    next_position[X]   += dT * math.cos(position[TH]) * self.motion[V]
    next_position[Y]   += dT * math.sin(position[TH]) * self.motion[V]
    next_position[TH]  += dT * self.motion[O]

    return next_position

  def draw_path(self, path):
    previous_point = self.round_point(path[0][0:2])
    for point in path:
      current_point = self.round_point(point[0:2])
      pygame.draw.line(self.screen, dt.REAL_PATH_COLOR, current_point, previous_point, 2)
      previous_point = current_point

  def draw_robot(self, coll_flag):
    # Colours for collision
    if coll_flag:
      robot_color = (255, 0, 0)
    else:
      robot_color = self.color

    # Body of the robot
    radius_robot = 0.5*self.axis_length
    center_robot = (self.round(self.position[X]), self.round_Y(self.position[Y]))
    pygame.draw.circle(self.screen, robot_color, center_robot, self.round(radius_robot), 2)

    # Head of the robot
    head_x_A = self.position[X] + (radius_robot * math.cos(self.position[TH]) * 1)
    head_y_A = self.position[Y] + (radius_robot * math.sin(self.position[TH]) * 1)
    head_x_B = self.position[X] + ((0.4*radius_robot) * math.cos(self.position[TH]) * 1)
    head_y_B = self.position[Y] + ((0.4*radius_robot) * math.sin(self.position[TH]) * 1)

    head_point_A = (self.round(head_x_A), self.round_Y(head_y_A))
    head_point_B = (self.round(head_x_B), self.round_Y(head_y_B))
    pygame.draw.line(self.screen, robot_color, head_point_A, head_point_B, 2)

  def update_position(self, wall_list, dT):
    coll_flag = False # collission flag
    radius_robot = 0.5 * self.axis_length

    # Calculating new X, Y & Orientation
    new_position = self.simplified_kinematics(self.position, dT)

    # Collision detection
    def check_collision(new_pos, wall_list, collision_flag):
      x, y, th = new_pos
      # create geometry of robot and path
      robot_center = Point(x, y).buffer(1)
      robot_shape = shapely.affinity.scale(robot_center, radius_robot, radius_robot)
      # print(robot_shape)
      traveled_line = LineString([(x, y), (self.position[X], self.position[Y])])

      wall_conflict = []
      for wall in wall_list:
        line_wall = LineString([wall[0], wall[1]])
        # print(wall[1])
        if robot_shape.intersects(line_wall) or traveled_line.intersects(line_wall):
          wall_conflict.append(wall)
          collision_flag = True
          # print(wall_conflict)
          if len(wall_conflict) >= 2:
            return [self.position[X], self.position[Y], th], collision_flag


          new = [x, y, th]
          velocity_vector = np.subtract(new, self.position)
          wall_vector = np.subtract(wall[0], wall[1])
          # If the wall and the velocity are not orthogonal, find the component of the velocity along the wall
          velocity_vector_xy = [velocity_vector[X], velocity_vector[Y]]
          if wall_vector.dot(velocity_vector_xy) != 0:
            norm_wall = wall_vector / np.linalg.norm(wall_vector)
            new_vel = norm_wall * np.dot(velocity_vector_xy, norm_wall)
            new_vel = np.append(new_vel, 0)
            new = np.add(self.position, new_vel)
            x = new[X]
            y = new[Y]
          else: # If they are orthogonal, put the robot as close as possible to the wall
            intersection_point = (0, 0)
            if robot_shape.intersects(line_wall):
              intersect_line = robot_shape.intersection(line_wall)
            else:
              intersect_line = traveled_line.intersection(line_wall)
            if len(intersect_line.coords) > 1:
              first_point = intersect_line.coords[0]
              second_point = intersect_line.coords[1]
              point_x = 0.5*(first_point[X] + second_point[X])
              point_y = 0.5*(first_point[Y] + second_point[Y])
              intersection_point = (point_x, point_y)
            elif intersect_line.geom_type == 'Point':
              intersection_point = intersect_line.coords[0]
            # Check that there's no division by 0
            if np.linalg.norm(velocity_vector) < 0.00001:
              x = self.position[X]
              y = self.position[Y]
            else:
              velocity_vector = radius_robot * (velocity_vector / np.linalg.norm(velocity_vector))
              x = intersection_point[X] - velocity_vector[X]
              y = intersection_point[Y] - velocity_vector[Y]

      return [x, y, th], collision_flag

    new_position, coll_flag = check_collision(new_position, wall_list, coll_flag)

    self.position = deepcopy(new_position)
    return coll_flag

  def robot_moving(self, wall_list, dt):
    collision_flag = self.update_position(wall_list, dt)
    self.draw_robot(collision_flag)
    return collision_flag

  def pose_tracking(self, ):
    localization.kalman_filter(self.motion)


  def draw_landmarks(self, wall_list, beacons):
    for beacon in beacons:
      collide = False
      point = Point(self.round(beacon[0]), self.round_Y(beacon[1]))
      # print (self.position)
      line = LineString([(self.round(self.position[0]),self.round_Y(self.position[1])), (self.round(beacon[0]), self.round_Y(beacon[1]))])
      distance = point.hausdorff_distance(line)
      print(distance)
      if distance < self.max_distance_sensor:
        pygame.draw.line(self.screen, (0, 255, 0), (self.round(self.position[0]), (self.round_Y(self.position[1]))),
                         (self.round(beacon[0]), self.round_Y(beacon[1])), 2)
        # TODO collision check
        # # print(rect)
        # for x,wall in enumerate(wall_list):
        #   line_wall = LineString([(self.round(wall[0][0]),self.round_Y(wall[0][1])),(self.round(wall[1][0]),self.round_Y(wall[1][1]))])
        #   if line.intersects(line_wall):
        #     collide = True
        #     pygame.draw.line(self.screen, (255, 0, 0), (self.round(self.position[0]), (self.round_Y(self.position[1]))),
        #                      (self.round(beacon[0]), self.round_Y(beacon[1])), 2)
        # if not collide:
        #   pass

    # for wall in wall_list:
    #     #   if rect.collidepoint()