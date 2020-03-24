import numpy as np
import math
X, Y, TH = 0, 1, 2

class Localization:
    def __init__(self, current_position, current_motion):
        self.position = current_position
        self.real_path = [current_position]
        self.current_mu = current_motion
        self.current_sigma = np.diagflat([.001, .002, .003])
        self.matrix_A = np.identity(3)
        self.matrix_C = np.identity(3)
        self.matrix_R = np.diagflat([.004, .005, .006])  # diagonal array init
        self.matrix_Q = np.diagflat([.007, .008, .009])

    def kalman_filter_prediction(self, position, motion, dT):
        # PREDICTION
        u = np.asarray(motion)
        u = u.T
        mu = np.array(self.current_mu)
        matrix_B = np.array([
            [dT * math.cos(position[TH]), 0],
            [dT * math.sin(position[TH]), 0],
            [0, dT],
        ])
        next_mu = np.dot(self.matrix_A, mu.T) + np.dot(matrix_B, u.T)
        next_sigma = np.dot(np.dot(self.matrix_A, self.current_sigma), self.matrix_A.T) + self.matrix_R

        return next_mu, next_sigma

    def update_localization(self, position, motion, dT):
        self.real_path.append(position)
        #next_mu, next_sigma = self.kalman_filter_prediction( position, motion, dT)
        # TODO inizio fai qualcosa
        #print("MU: ", next_mu)
        #print("SIGMA: ", next_sigma)



        # TODO fine fai qualcosa
        #self.current_mu = next_mu
        #self.current_sigma = next_sigma

    def triangulation(self,landmarks):
        print("landmarks")