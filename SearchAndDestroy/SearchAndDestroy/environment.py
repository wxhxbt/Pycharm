import numpy as np
import random


# generate the board for playing
def generate_board(dim):
    """
    :param dim: board size
    #0 ----> Flat
    #1 ----> Hilly
    #2 ----> Forest
    #3 ----> Caves
    :return:
    """
    m = np.zeros([dim, dim], dtype=int)
    for i in range(dim):
        for j in range(dim):
            m[i, j] = get_surface()
    return m


# set the probability of each cell
def get_surface():
    """
    :return:  a surface at random
    """
    p = np.random.rand()
    # create probability
    if 0 <= p <= 0.2:
        return 0
    if 0.2 < p <= 0.5:
        return 1
    if 0.5 < p <= 0.8:
        return 2
    if 0.8 < p <= 1.0:
        return 3


# the map of target in the board and not in the cell
Target_not_found_map = {0: 0.1, 1: 0.3, 2: 0.7, 3: 0.9}
Target_found_map = {0: 0.9, 1: 0.7, 2: 0.3, 3: 0.1}


# return the probability of not in the cell
def Target_not_found_given_Target_in_cell(cell_type):
    """
    :param cell_type: type of surface
    :return: probability that target not found give Target in cell
    """
    # 0 ----> Flat   ----> 0.1
    # 1 ----> Hilly  ----> 0.3
    # 2 ----> Forest ----> 0.7
    # 3 ----> Caves  ----> 0.9

    return Target_not_found_map[cell_type]


# create the position of the target for specific type
def Target_of_Type(board, type):
    """
    :param board: board
    :param type: type of surface
    :return: target in this type of surface
    """
    dim = len(board)
    a = random.randint(0, dim - 1)
    b = random.randint(0, dim - 1)
    while board[a, b] != type:
        a = random.randint(0, dim - 1)
        b = random.randint(0, dim - 1)
    return a, b


# initiate the matrix
def generate_initial_belief_matrix(dim):
    """
    :param dim: size of board
    :return: initial belief matrix
    """
    matrix = np.zeros([dim, dim]) + (1 / (dim * dim))
    return matrix


# choose the position of target
def choose_target(dim):
    pos = np.random.randint(1, dim * dim)
    i = pos % dim
    j = int(pos / dim) % dim
    return i, j


# update the belief matrix of board rule 1
def update_belief_matrix(board, belief, i, j):
    """
    :param i:
    :param board: board which contains type of terrain
    :param belief: belief matrix
    :param j: Failure in cell j
    :return: updated belief matrix
    """
    belief[i, j] = belief[i, j] * (Target_not_found_given_Target_in_cell(board[i, j]))
    normalization = np.sum(belief)
    belief = belief / normalization

    return belief


# initiate the probability of finding the target rule 2
def get_prob_found_matrix(board, belief):
    dim = len(board)
    prob_found_matrix = np.zeros([dim, dim])

    for i in range(dim):
        for j in range(dim):
            prob_found_matrix[i, j] = belief[i, j] * Target_found_map[board[i, j]]

    return prob_found_matrix
