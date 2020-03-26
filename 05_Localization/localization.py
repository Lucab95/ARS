import numpy as np
import math
from copy import deepcopy
from shapely.geometry import LineString, Point
import shapely
import data as dt

X, Y, TH = 0, 1, 2
V, O = 0, 1

class Localization:
    def __init__(self, init_position):
        self.position = init_position
        self.real_path = [init_position]
        self.mu_path = [init_position]
        self.last_mu = init_position
        self.last_sigma = np.diagflat([.001, .002, .003])
        self.matrix_A = np.identity(3)
        self.matrix_C = np.identity(3)
        self.matrix_R = np.diagflat([.004, .005, .006])  # diagonal array init
        self.matrix_Q = np.diagflat([.007, .008, .009])
        # self.z = []

    def kalman_filter_prediction(self, position, motion, sensor_estimate, dT):
        # PREDICTION
        predicted_mu = deepcopy(position)
        predicted_mu[X] += math.cos(position[TH]) * dT * motion[V]
        predicted_mu[X] += math.sin(position[TH]) * dT * motion[V]
        predicted_mu[X] += dT * motion[O]
        predicted_mu = np.vstack(predicted_mu)

        predicted_sigma = self.last_sigma + self.matrix_R

        # CORRECTION
        var1 = np.linalg.inv(predicted_sigma + self.matrix_Q)
        matrix_K = predicted_sigma * var1

        z = np.vstack(sensor_estimate)
        current_mu = predicted_mu + np.dot(matrix_K, (z - predicted_mu))

        current_sigma = np.dot((np.identity(3) - matrix_K), predicted_sigma)

        return np.hstack(current_mu).tolist(), current_sigma  # to put a horizontal list

    def update_localization(self, position, motion, dT):
        self.real_path.append(position)

        current_mu, current_sigma = self.kalman_filter_prediction(position, motion, position, dT)
        # TODO inizio fai qualcosa

        self.mu_path.append(current_mu)

        # TODO fine fai qualcosa
        self.last_mu = current_mu
        self.last_sigma = current_sigma

    def triangulation(self, landmarks):
        sensor1, sensor2, sensor3 = landmarks[0], landmarks[1], landmarks[2]  # [0 = [x,y], 1 = distance]]
        A = 2 * sensor2[0][0] - 2 * sensor1[0][0]
        B = 2 * sensor2[0][1] - 2 * sensor1[0][1]
        C = sensor1[1] ** 2 - sensor2[1] ** 2 - sensor1[0][0] ** 2 + sensor2[0][0] ** 2 - sensor1[0][1] ** 2 + \
            sensor2[0][1] ** 2
        D = 2 * sensor3[0][0] - 2 * sensor2[0][0]
        E = 2 * sensor3[0][1] - 2 * sensor2[0][1]
        F = sensor2[1] ** 2 - sensor3[1] ** 2 - sensor2[0][0] ** 2 + sensor3[0][0] ** 2 - sensor2[0][1] ** 2 + \
            sensor3[0][1] ** 2
        x = (C * E - F * B) / (E * A - B * D)
        y = (C * D - A * F) / (B * D - A * E)
        return x, y

    def calculate_degree(self, landmarks,position):
        # print(landmarks)
        # print(position)
        features = []
        z = []
        radius = 0.5 * dt.ROBOT_RADIUS
        robot_center = Point(position[X], position[Y]).buffer(1)
        robot_shape = shapely.affinity.scale(robot_center, radius, radius)

        for line in landmarks:
            intersection_point = robot_shape.intersection(line[0])
            # pygame.draw.circle(self.screen, (255, 100, 145), (self.round_point(intersection_point.coords[1])), 10, 2)
            beta = np.degrees(np.arctan2((intersection_point.coords[1][1] - position[1]),
                                         (intersection_point.coords[1][0] - position[0]))) #TODO remove this part and implement only via beacons
                                                                                                #with no intersection point
            x, y = self.get_robot_direction_point(position) #exact pose
            alfa = np.degrees(np.arctan2((y - position[1]), (x - position[0])))
            # alfa, beta = self.exact_degree(alfa, beta)
            # print(beta, alfa)
            theta = beta - alfa
            theta = self.exact_degree(theta)
            # print(theta)
            features.append([line[2][0], line[1]])  # [[x,y],distance]
            z.append([line[2][0][0], line[2][0][1], theta])  # [x, y, theta] wrong->#[distance,beacon_angle, beacon_idx]
            print("z", z)
        # print(features)
        # self.z = z
        return features

    def exact_degree(self, alfa):
        alfa = (alfa + 360) % 360;
        return alfa

    def get_robot_direction_point(self, position, radius = 1):
        x = position[X] + (radius * math.cos(position[2]) * 1)
        y = position[Y] + (radius * math.sin(position[2]) * 1)
        return (x, y)