from scipy.optimize import minimize
import numpy as np


class SVM:

    def __init__(self, train, h):
        self.h = h
        self.train = train
        self.dim = len(train[0][0])
        self.size = len(train)
        self.para = None

    def loss(self, x):
        """
        The loss function with L2 regularization
        :param x: parameters of the svm model whose size is equal to the size of training data
        :return: the value of loss
        """
        lamda = 0.1
        part1, part2 = 0, 0
        for i in range(self.size):
            s = 0
            for j in range(self.size):
                s = s + x[j] * self.kernel(self.train[i][0], self.train[j][0])
            part1 = part1 + np.square(self.train[i][1] - s)
            part2 = part2 + np.square(x[i])
        ls = part1 + lamda * part2
        return ls

    def kernel(self, x, y):
        """
        The kernel I used is Gaussian Kernel.
        """
        s = 0
        for i in range(self.dim):
            s = s + np.square(x[i] - y[i])
        return np.exp(-s/self.h)

    def train_model(self):
        """
        The training process is to find solution of unconstrained optimization problem
        and then we can get the optimal parameters of the model
        """
        fun = lambda x: self.loss(x)
        x0 = np.zeros(self.size)  # initialize
        res = minimize(fun, x0, method='SLSQP')
        self.para = res.x
        print('Optimum：', res.fun)
        print('Parameters：', res.x)
        print('Termination state：', res.success)
        print(res.message)

    def get_result(self, target):
        """
        Classify the target point by checking the sign of the function
        :param target: the target to be classified
        :return: the label of classification result
        """
        s = 0
        for i in range(self.size):
            s += self.para[i] * self.kernel(target, self.train[i][0])
        if s > 0:
            return 'A'
        else:
            return 'B'


def data_load():
    """
    function to load training data and test data
    :return: training_data, test_data
    """
    data, A, B, C = [], [], [], []
    with open('data.txt', 'r') as f:
        for line in f:
            data.append(list(map(int, line.split(','))))
    for i in range(5):
        # mark A as 1, mark B as -1
        A.append((data[i], 1))
        B.append((data[i + 5], -1))
        C.append(data[i + 10])
    return A+B, C


training_data, test_data = data_load()
svm = SVM(train=training_data, h=10)
svm.train_model()
for item in test_data:
    print(np.reshape(item, (5, 5)))
    print('Classified as:', svm.get_result(item), '\n')