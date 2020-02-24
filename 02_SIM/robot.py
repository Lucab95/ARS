# -*- coding: utf-8 -*-
"""
@author: Glauco
"""
import math

L, R = 0, 1
inf_number = math.pow(10,50)

class Robot():
  def __init__(self, length, max_v):
    self.axis_length = length
    self.max_v = max_v
    self.motor = [0, 0]

  # force value to stay in a range[min, max]
  def SetInARange(self, value, min, max):
    if value > self.max_v:
      value = self.max_v
    elif value < -self.max_v:
      value = -self.max_v
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
  def ForwardKinematics(self, x, y, th, dT):
    globalPos = [0, 0, 0]  # X' Y' th'

    if self.motor[R].velocity == self.motor[L].velocity:
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


  # TODO controlla
    def use_sensors(self, env):
      angle = self.direction
      # print(env)
      sensors = [None] * 12
      for i in range(12):
        # Draw lines
        sensor_x = int(self.position[0] + (self.length) * np.cos(
          np.radians(angle)))  # self.length indicates how long has to be the sensor outside of the circle
        sensor_y = int(self.position[1] + (self.length) * np.sin(np.radians(angle)))
        start_x = int(self.position[0] + (self.distance_sensors + self.length) * np.cos(np.radians(angle)))
        start_y = int(self.position[1]) + (self.distance_sensors + self.length) * np.sin(np.radians(angle))
        sensors[i] = (pygame.draw.line(screen, WHITE, (start_x, start_y), (sensor_x, sensor_y), 1))
        angle += 30
        # Check intersections
        self.value_sensors[i] = self.distance_sensors  # Initializing sensors values
        # Creating the sensor line
        line_sensor = LineString([sensors[i].topleft, sensors[i].bottomright])
        for j in range(len(env)):
          # Creating the environment line
          line_env = LineString([env[j].topleft, env[j].bottomright])
          # If collision -> Take value
          if str(line_sensor.intersection(line_env)) != "LINESTRING EMPTY":
            point = Point(self.position)
            self.value_sensors[i] = int(point.distance(line_sensor.intersection(line_env)) - self.length)

    def move_robot(self, sp, rot):
      # Change speed
      self.speed += sp
      # Change rotation
      self.rotation += rot
      self.draw_robot()

    def update_pos(self, limits_env):
      marg = 1
      # Updating direction
      self.direction = self.direction + self.rotation
      if self.direction < 0:
        self.direction = 359  # Limits in
      elif self.direction > 359:
        self.direction = 0  # the angtles
      # Updating position
      inc_x = self.speed * np.cos(np.radians(self.direction))
      inc_y = self.speed * np.sin(np.radians(self.direction))
      new_x = (self.position[0] + inc_x)
      new_y = (self.position[1] + inc_y)
      # COLLISION DETECTION
      # Checking limits environment
      if self.position[0] + self.length >= limits_env[0]:  # Right boundary
        new_x = limits_env[0] - self.length - marg
        print("Collision at time", time.time(), "in the position", self.position)
      elif self.position[0] - self.length <= limits_env[1]:  # Left boundary
        new_x = limits_env[1] + self.length + marg
        print("Collision at time", time.time(), "in the position", self.position)
      if self.position[1] + self.length >= limits_env[2]:  # Up boundary
        new_y = limits_env[2] - self.length - marg
        print("Collision at time", time.time(), "in the position", self.position)
      elif self.position[1] - self.length <= limits_env[3]:  # Down boundary
        new_y = limits_env[3] + self.length + marg
        print("Collision at time", time.time(), "in the position", self.position)
      # Updating position
      self.position = [new_x, new_y]

    def move_robot_complex(self, inc_right, inc_left):
      # Change velocity wheels
      self.speed_right += inc_right
      self.speed_left += inc_left
      # Change speed
      self.speed = (self.speed_right + self.speed_left) / 2
      # Calculating R (Point of Rotation)
      try:  # If both speeds are zero -> R = 0 (Error when diving by 0)
        self.R = (self.length / 2) * ((self.speed_left + self.speed_right) / (self.speed_right - self.speed_left))
      except:
        # self.R = np.inf
        self.R = 999999999999999999999999999999999999999999999999999999999999999
      # Calculating w (Rate Rotation or Rotation Angle)
      self.w = (
                         self.speed_right - self.speed_left) / self.length  # TODO probabilmente era questo che dava problemi perchè usava la lunghexza invece del raggio

    def update_pos_complex(self, limits_env):
      # Timesteps
      param = 2
      # Collission flag
      coll_flag = False
      # Calculating new X, Y & Orientation
      if self.speed_right != self.speed_left:
        # Calculating ICC
        ICC_x = self.position[0] - self.R * np.sin(np.radians(self.direction))
        ICC_y = self.position[1] - self.R * np.cos(np.radians(self.direction))
        # Matrixes involved
        rot_mat = np.asarray([[np.cos(self.w * param), -np.sin(self.w * param), 0],
                              [np.sin(self.w * param), np.cos(self.w * param), 0],
                              [0, 0, 1]])
        second_mat = [self.position[0] - ICC_x, self.position[1] - ICC_y, np.radians(self.direction)]
        third_mat = [ICC_x, ICC_y, self.w * param]
        # New coordinates and orientation
        new_x, new_y, new_dir = np.dot(rot_mat, second_mat) + third_mat
        self.direction = np.degrees(new_dir)
      else:
        # Updating position
        inc_x = self.speed * np.cos(np.radians(self.direction))
        inc_y = self.speed * np.sin(np.radians(self.direction))
        new_x = (self.position[0] + inc_x)
        new_y = (self.position[1] + inc_y)

      # Margin
      marg = 1
      # Limits of the angles
      if self.direction < 0:
        self.direction = 359  # Limits in
      elif self.direction > 359:
        self.direction = 0  # the angles

      # COLLISION DETECTION
      # Checking limits environment
      if self.position[0] + self.length >= limits_env[0]:  # Right boundary
        new_x = limits_env[0] - self.length - marg
        coll_flag = True
        print("Collision at time", time.time(), "in the position", self.position)
      elif self.position[0] - self.length <= limits_env[1]:  # Left boundary
        new_x = limits_env[1] + self.length + marg
        coll_flag = True
        print("Collision at time", time.time(), "in the position", self.position)
      if self.position[1] + self.length >= limits_env[2]:  # Up boundary
        new_y = limits_env[2] - self.length - marg
        coll_flag = True
        print("Collision at time", time.time(), "in the position", self.position)
      elif self.position[1] - self.length <= limits_env[3]:  # Down boundary
        new_y = limits_env[3] + self.length + marg
        coll_flag = True
        print("Collision at time", time.time(), "in the position", self.position)

      self.position = [new_x, new_y]
      return coll_flag

    def stop_robot(self):
      self.speed_right = 0
      self.speed_left = 0
      self.speed = 0
