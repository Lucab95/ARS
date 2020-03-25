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
import data
import localization

L, R = 0, 1
X, Y, TH = 0, 1, 2
V, O = 0, 1
inf_number = math.pow(10, 50)

class Robot:
    def __init__(self, screen, length, max_velocity, max_distance_sensor, start_position = [0, 0, 0]):
        self.screen = screen
        self.color = [90, 90, 90]
        self.position = start_position  # X Y THradians
        self.axis_length = length
        self.max_velocity = max_velocity
        self.motion = [0, 0]  # V, O
        self.max_distance_sensor = max_distance_sensor
        self.localization = localization.Localization(self.position)
        self.dir = [0,0]

    def round(self, value):
        return int(round(value))

    def round_Y(self, value):  # INVERT Y to get a right movement and axis origin
        return int(round(self.screen.get_size()[Y] - value))

    def round_point(self, point):  # INVERT Y to get a right movement and axis origin
        return (self.round(point[X]), self.round(self.screen.get_size()[Y] - point[Y]))

    def set_in_range(self, limit, value):  # force value to stay in a range[min, max]
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
        next_position[X] += dT * math.cos(position[TH]) * self.motion[V]
        next_position[Y] += dT * math.sin(position[TH]) * self.motion[V]
        next_position[TH] += dT * self.motion[O]

        return next_position

    def get_robot_direction_point(self, radius = 1):
        x = self.position[X] + (radius * math.cos(self.position[TH]) * 1)
        y = self.position[Y] + (radius * math.sin(self.position[TH]) * 1)
        return (x, y)

    def update_position(self, wall_list, dT):
        coll_flag = False  # collission flag
        radius_robot = 0.5 * self.axis_length

        # Calculating new X, Y & Orientation
        new_position = self.simplified_kinematics(self.position, dT)

        # Collision detection
        def check_collision(new_pos, wall_list, collision_flag):
            x, y, th = new_pos
            # create geometry of robot and path
            robot_center = Point(x, y).buffer(1)
            robot_shape = shapely.affinity.scale(robot_center, radius_robot, radius_robot)
            traveled_line = LineString([(x, y), (self.position[X], self.position[Y])])
            wall_conflict = []
            for wall in wall_list:
                line_wall = LineString([wall[0], wall[1]])
                if robot_shape.intersects(line_wall) or traveled_line.intersects(line_wall):
                    wall_conflict.append(wall)
                    collision_flag = True
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
                    else:  # If they are orthogonal, put the robot as close as possible to the wall
                        intersection_point = (0, 0)
                        if robot_shape.intersects(line_wall):
                            intersect_line = robot_shape.intersection(line_wall)
                        else:
                            intersect_line = traveled_line.intersection(line_wall)
                        if len(intersect_line.coords) > 1:
                            first_point = intersect_line.coords[0]
                            second_point = intersect_line.coords[1]
                            point_x = 0.5 * (first_point[X] + second_point[X])
                            point_y = 0.5 * (first_point[Y] + second_point[Y])
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

    def draw_robot(self, coll_flag):
        # Colours for collision
        if coll_flag:
            robot_color = (255, 0, 0)
        else:
            robot_color = self.color

        # Body of the robot
        radius_robot = 0.5 * self.axis_length
        center_robot = (self.round(self.position[X]), self.round_Y(self.position[Y]))
        pygame.draw.circle(self.screen, robot_color, center_robot, self.round(radius_robot), 2)

        # Head of the robot
        head_point_A = self.round_point(self.get_robot_direction_point(0.4 * radius_robot))
        head_point_B = self.round_point(self.get_robot_direction_point(radius_robot))
        pygame.draw.circle(self.screen, (255, 100, 145), (self.round_point(head_point_A)), 10, 2)
        self.dir = head_point_B
        # self.support_line = (head_point_A, (self.position[0] + radius_robot, head_point_A[1]))
        # print(head_point_B)
        pygame.draw.line(self.screen, robot_color, head_point_A, head_point_B, 2)
        # pygame.draw.line(self.screen, robot_color, self.support_line[0], self.support_line[1], 2) SUPPORT LINE

    def draw_path(self, path, color, segmented = False):
        previous_point = self.round_point(path[0][0:2])
        for index, point in enumerate(path):
            current_point = self.round_point(point[0:2])
            if segmented:
                if index % 10 < 6:
                    pygame.draw.line(self.screen, color, current_point, previous_point, 2)
            else:
                pygame.draw.line(self.screen, color, current_point, previous_point, 2)
            previous_point = current_point

    def draw_sensors(self, maze_walls, beacons):
        landmarks = []
        for beacon in beacons:
            # print(beacon[0], beacon[1])
            collide = False
            point = Point(beacon[0])
            # print (self.position)
            line = LineString([((self.position[0]), (self.position[1])),beacon[0]])
            distance = point.hausdorff_distance(line)
            # print(distance)
            if distance < self.max_distance_sensor:
                # pygame.draw.line(self.screen, (0, 255, 0), (self.round(self.position[0]), (self.round_Y(self.position[1]))),
                #                  (self.round(beacon[0]), self.round_Y(beacon[1])), 2)
                # TODO collision check
                # print(rect)
                for wall in maze_walls:
                    line_wall = LineString([(wall[0][0], wall[0][1]),
                                            (wall[1][0], wall[1][1])])
                    if line.intersects(line_wall):
                        # if beacon[0][0] != wall[0][0] and beacon[0][1] != wall[0][1]:
                        if not point.intersects(line_wall):
                            collide = True

                if not collide:
                    pygame.draw.line(self.screen, data.COLOR_SENSOR_LINE,
                                     (self.round(self.position[0]), (self.round_Y(self.position[1]))),
                                     (self.round_point(beacon[0])), 2)
                    landmarks.append([line, distance, beacon])
        return landmarks

    def robot_moving(self, walls, maze_walls, beacons, dt):
        self.localization.update_localization(self.position, self.motion, dt)
        collision_flag = self.update_position(walls, dt)
        self.draw_robot(collision_flag)
        self.draw_path(self.localization.real_path, data.REAL_PATH_COLOR)
        self.draw_path(self.localization.mu_path, data.MU_PATH_COLOR, True)


        landmarks = self.draw_sensors(maze_walls, beacons)
        if len(landmarks) >= 3:
            # print(landmarks)
            features = self.calculate_degree(landmarks)
            x,y= self.localization.triangulation(features)
            pygame.draw.circle(self.screen, (160, 235, 200), (self.round(x), self.round_Y(y)), 10, 2)
        return collision_flag

    def calculate_degree(self,landmarks):
        # print(landmarks)
        features = []
        # self.support_line
        # self.dir
        radius = 0.5*self.axis_length
        robot_center = Point(self.position[X],self.position[Y]).buffer(1)
        robot_shape = shapely.affinity.scale(robot_center,radius, radius)
        for line in landmarks:
            # print(line[0], robot_shape)

            # print(robot_shape.intersection(line[0]))
            intersection_point =robot_shape.intersection(line[0])
            # print(pos.coords[0])
            pygame.draw.circle(self.screen, (255, 100, 145), (self.round_point(intersection_point.coords[1])), 10, 2)
            beta = np.degrees(np.arctan2((intersection_point.coords[1][1]-self.position[1]),(intersection_point.coords[1][0]-self.position[0])))
            x,y = self.get_robot_direction_point()
            alfa = np.degrees(np.arctan2((y-self.position[1]),(x-self.position[0])))
            # alfa, beta = self.exact_degree(alfa, beta)
            # print(beta, alfa)
            theta = beta - alfa
            theta =self.exact_degree(theta)
            # print(theta)wwwww
            features.append([line[2][0],line[1]]) # [[x,y],distance]
            #TODO UTILIZZARE DOPO features.append([line[1], theta, line[2]]) #[distance,beacon_angle, beacon_idx]
        #print(features)
        return features

    def exact_degree(self,alfa):#,beta):
        alfa = (alfa + 360) % 360;
        # beta = (beta + 360) % 360;
        return alfa#,beta
