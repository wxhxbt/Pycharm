import numpy as np
import random
import copy


def is_rank_equal(matrix, r):
    num = np.linalg.matrix_rank(matrix)
    if num == r:
        return True
    else:
        return False


# Generate the random matrix of rank 3
rows, columns = 20, 5
rank = 3
array = [[0] * columns for i in range(rows)]
while not is_rank_equal(array, rank):
    all_columns = [x for x in range(columns)]
    random.shuffle(all_columns)
    random_columns = all_columns[:rank]
    duplicate_columns = all_columns[rank:]
    dup_targets = [random.choice(random_columns) for i in range(columns-rank)]
    coefficients = [random.randint(1, 9) for i in range(columns-rank)]

    for i in range(rows):
        for j in random_columns:
            array[i][j] = random.randint(1, 9)
    for i in range(rows):
        k = 0
        for j in duplicate_columns:
            array[i][j] = array[i][dup_targets[k]] * coefficients[k]
            k += 1
# for i in range(rows):
#     print(array[i])
print(is_rank_equal(array, rank))
original = copy.deepcopy(array)

# Decomposition using SVD
U, Sigma, Vt = np.linalg.svd(array)
print(Sigma)

# Randomly deleting elements N = 2, 3, 4, 5
shuffle = []
for i in range(20):
    for j in range(5):
        shuffle.append((i, j))
random.shuffle(shuffle)
for k in range(2, 6):
    shuffle0 = shuffle[:k]
    print("Zeros:", shuffle0)
    for cor in shuffle0:
        array[cor[0]][cor[1]] = 0

    # Matrix filling using SVD decomposition
    U, Sigma, Vt = np.linalg.svd(array)
    print(Sigma)
    print("new rank:", np.linalg.matrix_rank(array))
    Aprime = (U[:,0:rank]).dot(np.diag(Sigma[0:rank])).dot(Vt[0:rank,:])
    # for i in range(rows):
    #     print(Aprime[i])
    # Compute the error between original matrix and generated matrix
    error = 0.0
    for i in range(rows):
        for j in range(columns):
            error += abs(Aprime[i][j] - original[i][j])
            # error += np.square(abs(Aprime[i][j] - original[i][j]))
    print("total error:", error)
