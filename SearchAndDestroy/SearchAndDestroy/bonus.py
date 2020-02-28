from main import get_max_index
import numpy as np
import copy
import random
from environment import generate_board, generate_initial_belief_matrix, get_prob_found_matrix, update_belief_matrix, \
    Target_of_Type, Target_not_found_map


# Judge if the point is valid
def IsvalidPoint(dim, m, n):
    if m < 0 or n < 0 or m >= dim or n >= dim:
        return False
    return True


# get the list of neighbors of one node
def get_neighbors(dim, m, n):
    L = []
    new_L = []
    L.append([m - 1, n])
    L.append([m + 1, n])
    L.append([m, n - 1])
    L.append([m, n + 1])
    for l in L:
        if IsvalidPoint(dim, l[0], l[1]):
            new_L.append(l)
    return new_L


# target randomly move to another place
def move_target(dim, target, board):
    type_list = [0, 1, 2, 3]
    a = target[0]
    b = target[1]
    L = []
    new_L = []
    L.append([a - 1, b])
    L.append([a + 1, b])
    L.append([a, b - 1])
    L.append([a, b + 1])
    for l in L:
        if IsvalidPoint(dim, l[0], l[1]):
            new_L.append(l)
    new_pos = random.randint(1, len(new_L)) - 1
    type = board[new_L[new_pos][0], new_L[new_pos][1]]
    type_list.pop(type)
    return new_L[new_pos], random.choice(type_list)


def list_type(board, l, type):
    for i, j in l:
        if board[i, j] == type:
            return True
    return False


def update_found_matrix(board, prob_found_matrix, evidence):
    type = evidence
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i, j] == type:
                prob_found_matrix[i, j] = 0
            else:
                prob_found_matrix[i, j] = 1
    return prob_found_matrix


# compute sum of neighbors of a entrance
def neighbor_sum(matrix):
    dim = len(matrix)
    sum_matrix = np.zeros_like(matrix)
    for i in range(dim):
        for j in range(dim):
            # in the center of board
            if 0 < i < dim - 1 and 0 < j < dim - 1:
                sum_matrix[i, j] = matrix[i - 1, j] + matrix[i, j - 1] + matrix[i + 1, j] + matrix[i, j + 1]

            # corner of board
            elif i == 0 and j == 0:
                sum_matrix[i, j] = matrix[i + 1, j] + matrix[i, j + 1]
            elif i == dim - 1 and j == dim - 1:
                sum_matrix[i, j] = matrix[i - 1, j] + matrix[i, j - 1]
            elif i == 0 and j == dim - 1:
                sum_matrix[i, j] = matrix[i, j - 1] + matrix[i + 1, j]
            elif i == dim - 1 and j == 0:
                sum_matrix[i, j] = matrix[i - 1, j] + matrix[i, j + 1]

            # border of board
            elif i == 0:
                sum_matrix[i, j] = matrix[i, j - 1] + matrix[i + 1, j] + matrix[i, j + 1]
            elif i == dim - 1:
                sum_matrix[i, j] = matrix[i - 1, j] + matrix[i, j - 1] + matrix[i, j + 1]
            elif j == 0:
                sum_matrix[i, j] = matrix[i - 1, j] + matrix[i + 1, j] + matrix[i, j + 1]
            elif j == dim - 1:
                sum_matrix[i, j] = matrix[i - 1, j] + matrix[i, j - 1] + matrix[i + 1, j]
    return sum_matrix


# update the matrix of belief
# Belieft+1(x) = sum of x' Belieft(x')P(Xt+1=x|Xt=x')P(Yt+1|Xt+1=x)
# where x' belongs to S, S is the set of neighbors of x
def update_belief_matrix_new(board, prob_found_matrix, evidence):
    type = evidence
    new_prob_found_matrix = np.zeros_like(prob_found_matrix)
    for i in range(len(board)):
        for j in range(len(board)):
            current_type = board[i, j]
            if current_type == type:
                new_prob_found_matrix[i, j] = 0
            else:
                new_prob_found_matrix[i, j] = 1

    sum_matrix = neighbor_sum(new_prob_found_matrix)
    # a = prob_found_matrix * new_prob_found_matrix
    a = prob_found_matrix
    b = np.zeros_like(a)
    for i in range(len(a)):
        for j in range(len(a)):
            if sum_matrix[i, j] > 0:
                b[i, j] = a[i, j] / sum_matrix[i, j]
    f = neighbor_sum(b)
    return f


# new rule_1
def rule_1(board, belief_matrix, target):
    num_searches = 0
    dim = len(board)
    next_step = get_max_index(belief_matrix)
    prob = random.random()
    while (target[0], target[1]) != next_step or prob < Target_not_found_map[board[target[0], target[1]]]:
        belief_matrix = update_belief_matrix(board, belief_matrix, next_step[0], next_step[1])
        num_searches += 1
        target, evidence = move_target(dim, target, board)
        belief_matrix = update_belief_matrix_new(board, belief_matrix, evidence)
        for i in range(dim):
            for j in range(dim):
                if board[i][j] == evidence:
                    belief_matrix[i][j] = 0
        next_step = get_max_index(belief_matrix)
        prob = random.random()
    return num_searches


# new rule_2
def rule_2(board, belief_matrix, target):
    num_searches = 0
    dim = len(board)
    prob_found_matrix = get_prob_found_matrix(board, belief_matrix)
    next_step = get_max_index(prob_found_matrix)
    prob = random.random()
    while (target[0], target[1]) != next_step or prob < Target_not_found_map[board[target[0], target[1]]]:
        num_searches += 1
        belief_matrix = update_belief_matrix(board, belief_matrix, next_step[0], next_step[1])
        target, evidence = move_target(dim, target, board)
        belief_matrix = update_belief_matrix_new(board, belief_matrix, evidence)
        prob_found_matrix = get_prob_found_matrix(board, belief_matrix)
        for i in range(dim):
            for j in range(dim):
                if board[i][j] == evidence:
                    prob_found_matrix[i][j] = 0
        next_step = get_max_index(prob_found_matrix)
        prob = random.random()
    return num_searches


# new rule_3
def rule_3(board, belief_matrix, target):
    num_searches = 0
    dim = len(board)
    prob_found_matrix = get_prob_found_matrix(board, belief_matrix)
    next_step = get_max_index(prob_found_matrix)
    prob = random.random()
    dist = 0
    while (target[0], target[1]) != next_step or prob < Target_not_found_map[board[target[0], target[1]]]:
        num_searches += dist + 1
        belief_matrix = update_belief_matrix(board, belief_matrix, next_step[0], next_step[1])
        target, evidence = move_target(dim, target, board)
        belief_matrix = update_belief_matrix_new(board, belief_matrix, evidence)
        prob_found_matrix = get_prob_found_matrix(board, belief_matrix)
        for i in range(dim):
            for j in range(dim):
                if board[i][j] == evidence:
                    prob_found_matrix[i][j] = 0
        next_step, dist = get_optimal_solution(prob_found_matrix, next_step)
        prob = random.random()
    return num_searches


def get_optimal_solution(prob_mat, start):
    """
    function to find the coordinate of a grid which has the minimum cost
    :param prob_mat: matrix of P(target found in Cell_i)
    :param start: start point, search step in the last time point
    :return: coordinate of the Cell* and the distance from start to Cell*
    """
    min_value, min_cor, min_dist = find_first_element(prob_mat, start)
    for i in range(len(prob_mat)):
        for j in range(len(prob_mat)):
            if prob_mat[i, j] != 0:
                expectation = 1 / prob_mat[i, j]
                manhattan_dist = abs(i - start[0]) + abs(j - start[1])
                if min_value > expectation + manhattan_dist:
                    min_value = expectation + manhattan_dist
                    min_cor = (i, j)
                    min_dist = manhattan_dist
    return min_cor, min_dist


def find_first_element(prob_mat, start):
    for i in range(len(prob_mat)):
        for j in range(len(prob_mat)):
            if prob_mat[i, j] != 0:
                min_value = 1 / prob_mat[i, j] + abs(i - start[0]) + abs(j - start[1])
                min_cor = (i, j)
                min_dist = abs(i - start[0]) + abs(j - start[1])
                return min_value, min_cor, min_dist


def bonus_question():
    for type in [0, 1, 2, 3]:
        searches_rule1 = 0
        searches_rule2 = 0
        searches_rule3 = 0
        iterations = 1
        dim = 50
        for i in range(iterations):
            print("Calculating iteration", i+1, "...")
            board = generate_board(dim)
            target = Target_of_Type(copy.deepcopy(board), type)
            belief_matrix = generate_initial_belief_matrix(dim)
            # searches_rule1 += rule_1(copy.deepcopy(board), copy.deepcopy(belief_matrix), copy.copy(target))
            # searches_rule2 += rule_2(copy.deepcopy(board), copy.deepcopy(belief_matrix), copy.copy(target))
            searches_rule3 += rule_3(copy.deepcopy(board), copy.deepcopy(belief_matrix), copy.copy(target))
        # print("type :: " + str(type))
        # print("Average number of searches rule-1 and rule-2 respectively: ",
        #       str(searches_rule1 / iterations) + "  ,  " + str(searches_rule2 / iterations) + "\n")
        print("Average number of searches rule-3:", searches_rule3 / iterations)


bonus_question()
