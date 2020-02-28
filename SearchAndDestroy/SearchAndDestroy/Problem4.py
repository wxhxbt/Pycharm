from main import *


# New rule that always pick the grid which has the minimum cost
def rule_3(board, belief_matrix, target):
    num_searches = 0
    prob_found_matrix = get_prob_found_matrix(board=board, belief=belief_matrix)
    next_step = get_max_index(prob_found_matrix)
    prob = random.random()
    dist = 0
    while target != next_step or prob < Target_not_found_map[board[target[0], target[1]]]:
        belief_matrix = update_belief_matrix(board=board, belief=belief_matrix, i=next_step[0], j=next_step[1])
        num_searches += dist + 1
        prob_found_matrix = get_prob_found_matrix(board=board, belief=belief_matrix)
        next_step, dist = get_optimal_solution(prob_found_matrix, next_step)
        prob = random.random()
    return num_searches


# Compute the cost of every node, more specific:
# Cost_i = Manhattan distance from start to grid_i +
#                          Expectation of number of times to successfully discover the target in grid_i
def get_optimal_solution(prob_mat, start):
    """
    function to find the coordinate of a grid which has the minimum cost
    :param prob_mat: matrix of P(target found in Cell_i)
    :param start: start point, search step in the last time point
    :return: coordinate of the Cell* and the distance from start to Cell*
    """
    min_cor = (0, 0)
    min_dist = start[0] + start[1]
    min_value = 1 / prob_mat[0, 0] + start[0] + start[1]
    for i in range(len(prob_mat)):
        for j in range(len(prob_mat)):
            expectation = 1 / prob_mat[i, j]
            manhattan_dist = abs(i - start[0]) + abs(j - start[1])
            if min_value > expectation + manhattan_dist:
                min_value = expectation + manhattan_dist
                min_cor = (i, j)
                min_dist = manhattan_dist
    return min_cor, min_dist


def question_4():
    for t_type in [0, 1, 2, 3]:
        searches_rule_1 = 0
        searches_rule_2 = 0
        searches_rule_3 = 0
        iterations = 10
        dim = 20

        for i in range(iterations):
            # searches_rule_1 = 0
            # searches_rule_2 = 0
            # if i % 1 == 0:
            #    print(i)
            # generate board
            board = generate_board(dim)
            # Choose target
            target = Target_of_Type(copy.deepcopy(board), t_type)
            # print("target type  "+str(board[target[0],target[1]]))
            belief_matrix = generate_initial_belief_matrix(dim)
            searches_rule_1 += rule_1(copy.deepcopy(board), copy.deepcopy(belief_matrix), copy.copy(target))
            searches_rule_2 += rule_2(copy.deepcopy(board), copy.deepcopy(belief_matrix), copy.copy(target))
            searches_rule_3 += rule_3(copy.deepcopy(board), copy.deepcopy(belief_matrix), copy.copy(target))
            # print("rule-1 --- " + str(searches_rule_1) + "\t\trule-2 --- " + str(searches_rule_2)
            #     + "\t\trule-3 --- " + str(searches_rule_3))

        print("type :: " + str(t_type))
        print("Average number of searches rule-1, rule-2 and rule-3 respectively: ",
              str(searches_rule_1 / iterations) + "  ,  " + str(searches_rule_2 / iterations)
              + "  ,  " + str(searches_rule_3 / iterations) + "\n")


# before running question_4(), please make sure that question_3() in main.py has been commented.
question_4()
