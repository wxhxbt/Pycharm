import numpy as np


class K_NearestNeighbor:
    def __init__(self, train, k):
        self.k = k
        self.train = train
        self.dim = len(train[0][0])

    def get_distance(self, data, target):
        """
        Compute the distance between unclassified target and the data point
        :param data: the data point in training data set
        :param target: the target to be classified
        :return: Euclidean distance between them
        """
        dist = 0
        for i in range(self.dim):
            dist += np.square(data[i] - target[i])
        dist = np.sqrt(dist)
        return dist

    def get_neighbor(self, target):
        """
        Find the nearest points of the target
        :param target: the target to be classified
        :return: nearest points list of size k
        """
        self.train.sort(key=lambda x: self.get_distance(x[0], target))
        neighbors = self.train[:self.k]
        return neighbors

    def get_result(self, target):
        """
        Classify the target point
        :param target: the target to be classified
        :return: the label of classification result
        """
        nei_category = []
        for neighbor in self.get_neighbor(target):
            nei_category.append(neighbor[1])
        s = sum(nei_category)
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
knn = K_NearestNeighbor(train=training_data, k=5)
for item in test_data:
    print(np.reshape(item, (5, 5)))
    print('Classified as:', knn.get_result(item), '\n')

