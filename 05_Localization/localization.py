import numpy as np
import math


class Localization:
    def __init__(self, current_position, current_motion):
        self.position = current_position
        self.real_path = [current_position]
        self.mu = current_motion
        self.sigma = []

        self.matrix_A = np.identity(3)

        self.matrix_C = np.identity(3)

        self.matrix_R = np.diagflat([.1, .2, .3])  # diagonal array init
        self.matrix_Q = np.diagflat([.4, .5, .6])

    def get_maxtrix_B(self, orientation, dT):
        list = [
            [dT * math.cos(orientation), 0],
            [dT * math.sin(orientation), 0],
            [0, dT],
        ]
        return np.array(list)

    def next_mu_prediction(self, last_mu, motion, orientation, dT):
        u = np.array(motion).T
        matrix_B = self.get_maxtrix_B(orientation, dT)
        next_mu_pred = np.dot(self.matrix_A, last_mu) + np.dot(matrix_B, u)
        return next_mu_pred

    def next_sigma_prediction(self, last_sigma, last_matrix_R):
        return self.matrix_A * last_sigma * self.matrix_A.T + last_matrix_R

    def kalman_filter_prediction(self, last_mu, last_sigma, last_matrix_R, motion, orientation, dT):
        next_mu = self.next_mu_prediction(last_mu, motion, orientation, dT)
        next_sigma = self.next_sigma_prediction(last_sigma, last_matrix_R)

        return next_mu, next_sigma
