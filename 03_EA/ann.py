import numpy as np
import matplotlib.pyplot as plt


class ArtificialNeuralNetwork:

    def __init__(self, inputLayer, hiddenLayer, outputLayer):
        self.inputSize = inputLayer
        self.hiddenSize = hiddenLayer
        self.outputSize = outputLayer
        self.weights1 = np.random.randn(self.inputSize + 1,
                                        self.hiddenSize)  # Random weights at the beginning (One more for the bias)
        self.weights2 = np.random.randn(self.hiddenSize + 1,
                                        self.outputSize)  # Random weights at the beginning (One more for the bias)
        self.bias1 = 1
        self.bias2 = 1
        self.extraoutput_backprop = 1

    # Activation function
    def _bias_vector(self, length):
        spam = np.array([[self.bias]] * length)
        print("_bias_vector", spam)
        return spam

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # Forward propagation
    def forwardprop(self, x):
        x = np.concatenate((np.array([[self.bias1]] * len(x)), x), axis=1)  # Adding the first bias (input)
        self.hiddenLayer = self._sigmoid(np.dot(x, self.weights1))  # HiddenLayerActivation => Input x Weights1
        self.hiddenLayer = np.concatenate((np.array([[self.bias2]] * len(self.hiddenLayer)), self.hiddenLayer),
                                          axis=1)  # Adding the second bias (Hidden layer)
        output = self._sigmoid(np.dot(self.hiddenLayer, self.weights2))  # Output => HiddenLayerActivation x Weights2
        return output

    # Training weights
    def train(self, x, n_epochs):
        errors = []
        for i in range(0, n_epochs):
            output = self.forwardprop(x)
            errors.append([np.square(np.subtract(x, output)).mean(), i])

        errors = np.array(errors)
        plt.plot(errors[:, 1], errors[:, 0])
        plt.xlabel('Mean square error')
        plt.ylabel('Number epochs')
        plt.show()


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

train_data = dataset  # All

# Implementation
ANN = ArtificialNeuralNetwork(inputLayer=8, hiddenLayer=3, outputLayer=8)

# Training
ANN.train(train_data, 1000)
