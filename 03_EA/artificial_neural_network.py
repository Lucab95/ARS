import numpy as np
from copy import deepcopy

import matplotlib.pyplot as plt

#np.random.randn(self.inputSize, self.hiddenSize)

X, Y = 0, 1

class ArtificialNeuralNetwork:
    # create a 2 layers NN
    def __init__(self, n_inputs, n_hidden, n_outputs):
        self.inputSize = n_inputs
        self.hiddenSize = n_hidden
        self.outputSize = n_outputs
        self.weights_1L = np.ones((n_inputs, n_hidden))
        self.weights_2L = np.ones((n_hidden, n_outputs))
        self.bias_1L = np.ones((1, n_hidden))
        self.bias_2L = np.ones((1, n_outputs))

    def _random_weights(self, n, m):
        return np.random.randn(n, m)

    # Activation function
    def _bias_vector(self, length):
        spam = np.array([[self.bias_1L]] * length)
        print("_bias_vector", spam)
        return spam

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # Forward propagation
    def forward_propagation(self, inputs):
        print("\n\n1\n", inputs)
        hidden_layer = np.dot(inputs, self.weights_1L) + self.bias_1L
        hidden_layer = self._sigmoid(hidden_layer)
        print("\n\n3\n", hidden_layer)
        outputs = np.dot(hidden_layer, self.weights_2L) + self.bias_2L
        outputs = self._sigmoid(outputs)
        print("\n\n5\n", outputs)
        return outputs

    def mapping_input(self, input, input_range):  # [A,B] -> [0,1]
        new_input = []
        for inp in input:
            new_input.append(np.interp(inp, [input_range[0], input_range[1]], [0, 1]))
        return new_input

    def mapping_output(self, output, output_range):  #  [0,1] -> [A,B]
        new_output = []
        for out in output:
            X_new_out = np.interp(out[X], [0, 1], [output_range[X][0], output_range[X][1]])
            Y_new_out = np.interp(out[Y], [0, 1], [output_range[Y][0], output_range[Y][1]])
            new_output.append([X_new_out, X_new_out])
        return new_output

    # launch individual "life"
    #def start_ann_cicle(self, inputs, steps, output_range):
    #    for i in range(steps):
    #        outputs = self._forward_propagation(inputs)
    #        inputs = deepcopy(outputs)
    #        #inputs = self._mapping_output(outputs, output_range)
    #    return outputs
