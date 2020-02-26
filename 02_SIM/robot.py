# -*- coding: utf-8 -*-
"""
@author: Glauco
"""
from copy import deepcopy
import math
import pygame
from shapely.geometry import LineString, Point

X, Y, th = 0, 1, 2
L, R = 0, 1
inf_number = math.pow(10,50)

class Robot():
  def __init__(self, length, max_velocity):
    self.position = [0, 0, 0] #X Y Th
    self.axis_length = length
    self.max_velocity = max_velocity
    self.motor = [10, 0]
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

  def use_sensors(self, screen, env):
    angle = self.position[th]
    sensors = [None] * 12
    distance_sensor = 200
    for i in range(12):
      # create lines
      sensor_x = self.position[X] + 0.5 * self.axis_length * math.cos(angle)
      sensor_y = self.position[Y] + 0.5 * self.axis_length * math.sin(angle)

      start_x = self.position[X] + (0.5 * self.axis_length + distance_sensor) * math.cos(angle)
      start_y = self.position[Y] + (0.5 * self.axis_length + distance_sensor) * math.sin(angle)

      pointA = (self.round(start_x), self.round_Y(screen, start_y))
      pointB = (self.round(sensor_x), self.round_Y(screen, sensor_y))

      sensors[i] = (pygame.draw.line(screen, (255, 0, 0), pointA, pointB, 1))

      # Check intersections
      self.sensor_list[i] = distance_sensor  # Initializing sensors values

      # Creating the sensor line
      line_sensor = LineString([sensors[i].topleft, sensors[i].bottomright])
      for j in range(len(env)):
        # Creating the environment line
        line_env = LineString([env[j].topleft, env[j].bottomright])
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
    coord_robot = pygame.draw.circle(screen, robot_color, center_robot, self.round(0.5*self.axis_length), 2)

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
        self.position[X] + (0.5*self.axis_length * math.cos(angle) * 1.2),
        self.position[Y] + (0.5*self.axis_length * math.sin(angle) * 1.2),
        18
      )
      angle += math.radians(30)

    # set motor labels
    RobotLabel(
      self.motor[L],
      self.position[X] + (0.5*self.axis_length * math.cos(self.position[th] - math.radians(90)) * 0.4),
      self.position[Y] + (0.5*self.axis_length * math.sin(self.position[th] - math.radians(90)) * 0.4),
      18
    )
    RobotLabel(
      self.motor[R],
      self.position[X] + (0.5*self.axis_length * math.cos(self.position[th] + math.radians(90)) * 0.4),
      self.position[Y] + (0.5*self.axis_length * math.sin(self.position[th] + math.radians(90)) * 0.4),
      18
    )
    return coord_robot

  def update_position(self, limits_env, dT):

    # Collission flag
    coll_flag = False

    # Calculating new X, Y & Orientation
    new_position = self._ForwardKinematics(self.position[X], self.position[Y], self.position[th], dT)

    # Margin
    margin_pixels = 0

    # COLLISION DETECTION Checking limits environment
    robot_radius = 0.5*self.axis_length
    if new_position[X] + robot_radius >= limits_env[0]:  # Right boundary
      new_position[X] = limits_env[0] - robot_radius - margin_pixels
      coll_flag = True
    elif new_position[X] - robot_radius <= limits_env[1]:  # Left boundary
      new_position[X] = limits_env[1] + robot_radius + margin_pixels
      coll_flag = True

    if new_position[Y] + robot_radius >= limits_env[2]:  # Up boundary
      new_position[Y] = limits_env[2] - robot_radius - margin_pixels
      coll_flag = True
    elif new_position[Y] - robot_radius <= limits_env[3]:  # Down boundary
      new_position[Y] = limits_env[3] + robot_radius + margin_pixels
      coll_flag = True

    self.position = deepcopy(new_position)
    return coll_flag