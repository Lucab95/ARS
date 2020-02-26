# -*- coding: utf-8 -*-
"""
@author: Glauco
"""
from copy import deepcopy
import math
import pygame
from shapely.geometry import LineString, Point

import pygame
import numpy as np
import shapely
from shapely.geometry import LineString, Point
from shapely import affinity
import math as m

X, Y, th = 0, 1, 2
L, R = 0, 1
inf_number = math.pow(10,50)

class Robot():
  def __init__(self, length, max_velocity, max_distance_sensor):
    self.position = [0, 0, 0] #X Y Th
    self.axis_length = length
    self.max_velocity = max_velocity
    self.max_distance_sensor = max_distance_sensor
    self.motor = [0, 0]
    self.color = [90, 90, 90]
    self.sensor_list = [0] * 12

  # force value to stay in a range[min, max]
  def SetInARange(self, value):
    if value > self.max_velocity:
      value = self.max_velocity
    elif value < -self.max_velocity:
      value = -self.max_velocity
    return value

  def NewMotorVelocity(self, n_motor, value):
    self.motor[n_motor] = self.SetInARange(value)

  def ChangeMotorVelocity(self, n_motor, value):
    next_value = self.motor[n_motor] + value
    self.motor[n_motor] = self.SetInARange(next_value)

  def _omega(self):
    return (self.motor[R] - self.motor[L]) / self.axis_length

  def _R(self):
    diff_V = self.motor[R] - self.motor[L]
    if diff_V == 0:
      return inf_number #math.inf # inf_number
    else:
      return 0.5 * self.axis_length * (self.motor[R] + self.motor[L]) / diff_V

  # NOTE: in radians
  def _ICC(self, x, y, th):
    return [x - self._R() * math.sin(th), y + self._R() * math.cos(th)]

  # NOTE: in radians
  def _ForwardKinematics(self, x, y, th, dT):
    globalPos = [0, 0, 0]  # X' Y' th'

    if self.motor[R] == self.motor[L]:
      globalPos[0] = x + self.motor[R] * math.cos(th) * dT
      globalPos[1] = y + self.motor[R] * math.sin(th) * dT
      globalPos[2] = th
    else:
      odt = self._omega() * dT
      ICC = self._ICC(x, y, th)
      SIN_odt = math.sin(odt)
      COS_odt = math.cos(odt)
      globalPos[0] = (COS_odt*(x - ICC[0]) - SIN_odt*(y - ICC[1])) + ICC[0]
      globalPos[1] = (SIN_odt*(x - ICC[0]) + COS_odt*(y - ICC[1])) + ICC[1]
      globalPos[2] = th + odt

    return globalPos

  def round(self, value):
    return int(round(value))

  def round_Y(self, screen, value): # INVERT Y to get a right movement and axis origin
    return int(round(screen.get_size()[Y] - value))

  def use_sensors(self, screen, wall_list):
    angle = self.position[th]

    for i in range(len(self.sensor_list)):
      # Initializing sensors values
      self.sensor_list[i] = self.max_distance_sensor

      # create two point of the sensor line
      sensor_x = self.position[X] + 0.5 * self.axis_length * math.cos(angle)
      sensor_y = self.position[Y] + 0.5 * self.axis_length * math.sin(angle)

      start_x = self.position[X] + (0.5 * self.axis_length + self.max_distance_sensor) * math.cos(angle)
      start_y = self.position[Y] + (0.5 * self.axis_length + self.max_distance_sensor) * math.sin(angle)

      sensor_points = [(sensor_x, sensor_y), (start_x, start_y)]

      pointA = (self.round(start_x), self.round_Y(screen, start_y))
      pointB = (self.round(sensor_x), self.round_Y(screen, sensor_y))

      pygame.draw.line(screen, (255, 0, 0), pointA, pointB, 1)

      # Creating the sensor line
      #asd = [sensors[i].topleft, sensors[i].bottomright]
      line_sensor = LineString([sensor_points[0], sensor_points[1]])
      for wall in wall_list:
        # Creating the environment line
        line_env = LineString([wall[0], wall[1]])
        # If collision -> Take value
        if str(line_sensor.intersection(line_env)) != "LINESTRING EMPTY":
          point = Point((self.position[X], self.position[Y]))
          self.sensor_list[i] = self.round(point.distance(line_sensor.intersection(line_env)) - self.axis_length)

      angle += math.radians(30)

  def draw_robot(self, screen, coll_flag):
    # Colours for collision
    if coll_flag:
      robot_color = (255, 0, 0)
    else:
      robot_color = self.color

    # Body of the robot
    center_robot = (self.round(self.position[X]), self.round_Y(screen, self.position[Y]))
    pygame.draw.circle(screen, robot_color, center_robot, self.round(0.5*self.axis_length), 2)

    # Head of the robot
    head_x = self.position[X] + (0.5*self.axis_length * math.cos(self.position[th]) * 1)
    head_y = self.position[Y] + (0.5*self.axis_length * math.sin(self.position[th]) * 1)

    head_point = (self.round(head_x), self.round_Y(screen, head_y))
    pygame.draw.line(screen, robot_color, center_robot, head_point, 2)

    def RobotLabel(value, x, y, font_size):
      font = pygame.font.SysFont("dejavusans", font_size)
      label = font.render(str(format(value, '.0f')), True, (0,0,0))
      posX = x - 0.5*label.get_rect().width
      posY = y + 0.5*label.get_rect().height
      screen.blit(label, (self.round(posX),self.round_Y(screen, posY)))

    # Sensors of the robot
    angle = self.position[th]
    for val in self.sensor_list:
      RobotLabel(
        val,
        self.position[X] + (0.5*self.axis_length * math.cos(angle) * 1.5),
        self.position[Y] + (0.5*self.axis_length * math.sin(angle) * 1.5),
        18
      )
      angle += math.radians(30)

    # set motor labels
    RobotLabel(
      self.motor[L],
      self.position[X] + (0.5*self.axis_length * math.cos(self.position[th] + math.radians(90)) * 0.4),
      self.position[Y] + (0.5*self.axis_length * math.sin(self.position[th] + math.radians(90)) * 0.4),
      18
    )
    RobotLabel(
      self.motor[R],
      self.position[X] + (0.5*self.axis_length * math.cos(self.position[th] - math.radians(90)) * 0.4),
      self.position[Y] + (0.5*self.axis_length * math.sin(self.position[th] - math.radians(90)) * 0.4),
      18
    )

  def update_position(self, wall_list, dT):

    # Collission flag
    coll_flag = False

    # Calculating new X, Y & Orientation
    new_position = self._ForwardKinematics(self.position[X], self.position[Y], self.position[th], dT)

    # COLLISION DETECTION Checking limits environment
    def along_wall(vel_vec, wall_vec):
      norm_wall = wall_vec / np.linalg.norm(wall_vec)
      new_vel = norm_wall * np.dot(vel_vec, norm_wall)
      return new_vel
#
    def check_collision(x, y, th, wall_list):
      robot_center = Point(x, y).buffer(1)
      robot_shape = shapely.affinity.scale(robot_center, 0.5*self.axis_length, 0.5*self.axis_length)
      traveled_line = LineString([(x, y), (self.position[X], self.position[Y])])
      wall_conflict = []
      for wall in wall_list:
        line_wall = LineString([wall[0], wall[1]])
        if robot_shape.intersects(line_wall) or traveled_line.intersects(line_wall):
          # If the robot intersects with more than one wall, it's in a corner and should stay there
          if len(wall_conflict) > 0:
            return self.position[X], self.position[Y], th
          new = [x, y, th]
          velocity_vector = np.subtract(new, self.position)
          wall_vector = np.subtract(wall[0], wall[1])
          # If the wall and the velocity are not orthogonal, find the component of the velocity along the wall
          if wall_vector.dot([velocity_vector[0], velocity_vector[1]]) != 0:
            new_vel = along_wall([velocity_vector[0], velocity_vector[1]], wall_vector)
            new_vel = np.append(new_vel, 0)
            new = np.add(self.position, new_vel)
            x = new[0]
            y = new[1]
          # If they are orthogonal, put the robot as close as possible to the wall
          else:
            intersection_point = (0, 0)
            if robot_shape.intersects(line_wall):
              intersect_line = robot_shape.intersection(line_wall)
            else:
              intersect_line = traveled_line.intersection(line_wall)
            if len(intersect_line.coords) > 1:
              first_point = intersect_line.coords[0]
              second_point = intersect_line.coords[1]
              point_x = (first_point[0] + second_point[0]) / 2
              point_y = (first_point[1] + second_point[1]) / 2
              intersection_point = (point_x, point_y)
            elif intersect_line.geom_type == 'Point':
              intersection_point = intersect_line.coords[0]
            # Check that there's no division by 0
            if np.linalg.norm(velocity_vector) < 0.00001:
              x = self.position[X]
              y = self.position[Y]
            else:
              velocity_vector = 0.5*self.axis_length * (velocity_vector / np.linalg.norm(velocity_vector))
              x = intersection_point[0] - velocity_vector[0]
              y = intersection_point[1] - velocity_vector[1]
          wall_conflict.append(wall)
      return x, y, th

    new_position = check_collision(new_position[X],new_position[Y],new_position[th], wall_list)

    self.position = deepcopy(new_position)
    return coll_flag

  def robot_moving(self, screen, wall_list, dt):
    collision_flag = self.update_position(wall_list, dt)
    self.use_sensors(screen, wall_list)
    self.draw_robot(screen, collision_flag)