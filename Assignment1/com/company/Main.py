__author__ = 'Frank Wang'

from com.company.Solution import *
from com.company.HardMaze import *
import numpy as np
import time


# -----------------------------------------------------------------------------------------------
#
def test_single(dim, p, method):
    """
    Function to test each algorithm one time.
    """
    maze = Maze(dim, p)
    maze.build_maze()
    # maze.show_maze_with_p()
    matrix = maze.get_matrix()
    t = choose_method(dim, method, matrix)
    sol_set = t[0]
    nodes_expanded = t[1]
    max_fringe = t[2]
    if sol_set is None:
        # print("There is no solution for this maze.")
        return None
    else:
        print("Shortest path: ",len(sol_set),"Nodes expanded:",nodes_expanded,"Max fringe size:",max_fringe)
        # maze.show_solution(sol_set)
        return len(sol_set)


# -----------------------------------------------------------------------------------------------
#
def test_average_runtime(p, times, method):
    for dim in range(100, 1001, 100):
        average_time = 0
        for i in range(times):
            start = time.time()
            test_single(dim, p, method)
            end = time.time()
            average_time += (end - start)/times
        print("Dimension: ", dim, "\tAverage runtime: ", average_time)


# -----------------------------------------------------------------------------------------------
#
def test_solvability(scale_times, method):
    set_p = np.arange(0.3, 0.4, 0.01)
    for p in set_p:
        suc = 0
        for i in range(scale_times):
            if test_single(200, p, method):
                suc += 1
        print("Density: ", p, "Solvability: ", suc/scale_times)


# -----------------------------------------------------------------------------------------------
#
def test_expect_path_length(max_p, scale_times, method):
    set_p = np.arange(0, max_p+max_p/10, max_p/10)
    for p in set_p:
        suc = 0
        exp_length = 0
        while suc < scale_times:
            ret_num = test_single(300, p, method)
            if ret_num:
                suc += 1
                exp_length += ret_num/scale_times
        print("Density: ", p, " Expected shortest path length: ", exp_length)


def choose_method(dim, method, matrix):

    sol = Solution(matrix)
    start, end = (0, 0), (dim-1, dim-1)
    if method == 'dfs': return sol.depth_first_search(start, end)
    elif method == 'bfs': return sol.breadth_first_search(start, end)
    elif method == 'bibfs': return sol.bidirectional_breadth_first_search(start, end)
    elif method == 'AstarM': return astar_search(matrix, dim, 'Manhattan')
    elif method == 'AstarE': return astar_search(matrix, dim, 'Euclid')
    else: return None


# -----------------------------------------------------------------------------------------------
#
def get_the_hardest(nums, dim, p, p_m1, p_m2):
    hardest_maze = generate_hard_maze(nums, dim, p, p_m1, p_m2)
    maze = Maze(dim, p)
    maze.set_matrix(hardest_maze[0])
    s = Solution(hardest_maze[0])
    # sol = s.breadth_first_search((0, 0), (dim-1, dim-1))
    # sol = s.depth_first_search((0, 0), (dim - 1, dim - 1))
    sol = astar_search(hardest_maze[0], dim, "Manhattan")
    # maze.show_solution(sol[0])
    print("second search:", len(sol[0]), sol[1], sol[2])
    print("Total blocks:", maze.get_actual_p())
    return sol, hardest_maze


# -----------------------------------------------------------------------------------------------
#
def test_mutation():
    set_p1 = np.arange(0.7, 1, 0.1)
    set_p2 = np.arange(0.1, 0.21, 0.1)
    for p1 in set_p1:
        for p2 in set_p2:
            f = open("MutationResult.txt", 'a')
            sol, hardest_maze = get_the_hardest(30, 100, 0.35, p1, p2)
            # f.write(' 0 \t\t\t'+str(p2))
            f.write(' ' + str(p1) + '\t\t\t ' + str(p2))
            f.write('\t\t\t\t\t'+str(len(sol[0]))+'\t\t'+str(sol[1])+'\t\t'+str(sol[2])+'\n')
            f.write(str(hardest_maze[0])+'\n')
            f.close()


# -----------------------------------------------------------------------------------------------
#
if __name__ == '__main__':
    # test_average_runtime(0.1, 1, 'AstarM')
    # test_solvability(100, 'dfs')
    # test_expect_path_length(0.3, 10, 'bfs')
    # test_average_runtime_astar(0.2, "AsterE")
    # while True:
    #     test_single(100, 0.01, 'AstarM')
    # get_the_hardest(50, 100, 0.35)
    test_mutation()

