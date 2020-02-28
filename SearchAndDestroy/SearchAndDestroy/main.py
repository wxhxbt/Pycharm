import numpy as np
import copy
from environment import generate_board, generate_initial_belief_matrix, get_prob_found_matrix, update_belief_matrix, \
    Target_of_Type
import random


# the map of target in the board and not in the cell
Target_not_found_map = {0: 0.1, 1: 0.3, 2: 0.7, 3: 0.9}
Target_found_map = {0: 0.9, 1: 0.7, 2: 0.3, 3: 0.1}


def get_max_index(prob_mat):
    """
    :param prob_mat: probability matrix
    :return: returns index which has maximum probability
    """
    max_value = np.ndarray.max(prob_mat)
    result = []
    for i in range(len(prob_mat)):
        for j in range(len(prob_mat)):
            if prob_mat[i, j] == max_value:
                result.append((i, j))
    a = random.randint(1, len(result)) - 1
    return result[a]


# rule 1
def rule_1(board, belief_matrix, target):
    num_searches = 0
    next_step = get_max_index(belief_matrix)
    prob = random.random()
    while target != next_step or prob < Target_not_found_map[board[target[0], target[1]]]:
        belief_matrix = update_belief_matrix(board=board, belief=belief_matrix, i=next_step[0], j=next_step[1])
        num_searches += 1
        next_step = get_max_index(belief_matrix)
        prob = random.random()
    return num_searches


# rule 2
def rule_2(board, belief_matrix, target):
    num_searches = 0
    prob_found_matrix = get_prob_found_matrix(board=board, belief=belief_matrix)
    next_step = get_max_index(prob_found_matrix)
    prob = random.random()
    while target != next_step or prob < Target_not_found_map[board[target[0], target[1]]]:
        belief_matrix = update_belief_matrix(board=board, belief=belief_matrix, i=next_step[0], j=next_step[1])
        num_searches += 1
        prob_found_matrix = get_prob_found_matrix(board=board, belief=belief_matrix)
        next_step = get_max_index(prob_found_matrix)
        prob = random.random()
    return num_searches


def question_3():
    for t_type in [0, 1, 2, 3]:
        searches_rule_1 = 0
        searches_rule_2 = 0
        iterations = 20
        dim = 50

        for i in range(20):
            # searches_rule_1 = 0
            # searches_rule_2 = 0
            # generate board
            board = generate_board(dim)
            # Choose target
            target = Target_of_Type(copy.deepcopy(board), t_type)
            # print("target type  "+str(board[target[0],target[1]]))
            belief_matrix = generate_initial_belief_matrix(dim)
            searches_rule_1 += rule_1(copy.deepcopy(board), copy.deepcopy(belief_matrix), copy.copy(target))
            searches_rule_2 += rule_2(copy.deepcopy(board), copy.deepcopy(belief_matrix), copy.copy(target))

        print("type :: " + str(t_type))
        print("Average number of searches rule-1 and rule-2 respectively: ",
              str(searches_rule_1 / iterations) + "  ,  " + str(searches_rule_2 / iterations) + "\n")

# question_3()
