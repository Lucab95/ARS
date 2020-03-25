import numpy as np
import math
from copy import deepcopy
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

    def kalman_filter_prediction(self, position, motion, sensor_estimate, dT):
        # PREDICTION
        predicted_mu = deepcopy(position)
        predicted_mu[X] += math.cos(position[TH]) * dT * motion[V]
        predicted_mu[X] += math.sin(position[TH]) * dT * motion[V]
        predicted_mu[X] += dT * motion[O]
        predicted_mu = np.vstack(predicted_mu)

        predicted_sigma = self.last_sigma + self.matrix_R

        #CORRECTION
        var1 = np.linalg.inv(predicted_sigma + self.matrix_Q)
        matrix_K = predicted_sigma * var1

        z = np.vstack(sensor_estimate)
        current_mu = predicted_mu + np.dot(matrix_K, (z - predicted_mu))

        current_sigma = np.dot((np.identity(3) - matrix_K), predicted_sigma)

        return np.hstack(current_mu).tolist(), current_sigma # to put a horizontal list

    def update_localization(self, position, motion, dT):
        self.real_path.append(position)
        current_mu, current_sigma = self.kalman_filter_prediction(position, motion, position, dT)
        # TODO inizio fai qualcosa


        self.mu_path.append(current_mu)

        # TODO fine fai qualcosa
        self.last_mu = current_mu
        self.last_sigma = current_sigma

    def triangulation(self,landmarks):
        print("landmarks")
        sensor1, sensor2, sensor3 = landmarks[0], landmarks[1], landmarks[2] # [0 = [x,y], 1 = distance]]
        A= 2 * sensor2[0][0] - 2* sensor1[0][0]
        B= 2 * sensor2[0][1] - 2* sensor1[0][1]
        C = sensor1[1]**2 - sensor2[1]**2 - sensor1[0][0]**2 + sensor2[0][0]**2 -sensor1[0][1]**2 + sensor2[0][1]**2
        D = 2 * sensor3[0][0] - 2* sensor2[0][0]
        E = 2 * sensor3[0][1] - 2 * sensor2[0][1]
        F = sensor2[1] ** 2 - sensor3[1] ** 2 - sensor2[0][0] ** 2 + sensor3[0][0] ** 2 - sensor2[0][1] ** 2 + sensor3[0][1] ** 2
        x = (C*E - F*B) / (E * A - B *D)
        y = (C*D - A*F) / (B*D - A*E)
        return x, y