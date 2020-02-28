import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

#np.random.randn(self.inputSize + 1, self.hiddenSize)

class ArtificialNeuralNetwork:
    # create a 2 layers NN
    def __init__(self, n_inputs, n_hidden, n_outputs):
        self.inputSize = n_inputs
        self.hiddenSize = n_hidden
        self.outputSize = n_outputs
        self.weights_1L = np.zeros((n_inputs, n_hidden))
        self.weights_2L = np.zeros((n_hidden, n_outputs))
        self.bias_1L = np.ones((1, n_hidden))
        self.bias_2L = np.ones((1, n_outputs))


    def _random_weights(self, n, m):
        return np.random.randn(n + 1, m)


    # Activation function
    def _bias_vector(self, length):
        spam = np.array([[self.bias_1L]] * length)
        print("_bias_vector", spam)
        return spam

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # Forward propagation
    def _forward_propagation(self, inputs):
        hidden_layer = self._sigmoid(np.dot(inputs, self.weights_1L))
        outputs = self._sigmoid(np.dot(hidden_layer, self.weights_2L))
        return outputs

    # launch individual "life"
    def start_individual(self, inputs, steps, output_range):
        #errors = []
        for i in range(steps):
            outputs = self._forward_propagation(inputs)
            # TODO rimettere xy nella forma normale
            #from numpy import interp

            outputs[0] = np.interp(outputs[0], [0, 1], [output_range[0], output_range[1]])
            outputs[1] = np.interp(outputs[1], [0, 1], [output_range[0], output_range[1]])
            inputs = outputs
            #errors.append([np.square(np.subtract(x, output)).mean(), i])

        return outputs
        #errors = np.array(errors)
        #plt.plot(errors[:, 1], errors[:, 0])
        #plt.xlabel('Mean square error')
        #plt.ylabel('Number epochs')
        #plt.show()


# Creation dataset
dataset = np.array(
    [
     [1, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 1, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 1]
    ]
)

train_data = deepcopy(dataset)  # All

# Implementation
ANN = ArtificialNeuralNetwork(2, 4, 2)

print(ANN.weights_1L)
print(ANN.weights_2L)
print(ANN.bias_1L)
print(ANN.bias_2L)
# Training
#ANN.start_individual(train_data, 1000)
