from random import random
import matplotlib.pyplot as plt
import copy


class Maze:
    # -----------------------------------------------------------------------------------------------
    #
    def __init__(self, dim=100, p=0.5):
        """
        :param dim: The dimension of a square maze
        :param p: The portion of the occupied cells in the maze excluding the upper left and lower right corners
        """
        self._dim = dim
        self._p = p
        self._maze = [[-1] * self._dim for i in range(0, self._dim)]

    # -----------------------------------------------------------------------------------------------
    #
    def build_maze(self):
        """
        Build the maze according to the dimension and probability of p.
        :return:
        """
        for i in range(0, self._dim):
            for j in range(0, self._dim):
                if i == 0 and j == 0: continue
                if i == self._dim - 1 and j == self._dim - 1: continue
                x = random()
                if x < self._p:
                    self._maze[i][j] = 1
                else:
                    self._maze[i][j] = 0
        self._maze[0][0] = 0
        self._maze[self._dim-1][self._dim-1] = 0

    # -----------------------------------------------------------------------------------------------
    #
    def show_maze_with_p(self):
        """
        Show result of the built maze in the form of graph.
        Different color represents different state(free or blocked).
        """
        # for i in range(0, self._dim):
        #     print(self._maze[i])
        plt.figure('Maze with p=' + str(self._p))
        plt.imshow(self._maze)
        plt.show()

    # -----------------------------------------------------------------------------------------------
    ##
    def get_matrix(self):
        return self._maze

    # -----------------------------------------------------------------------------------------------
    ##
    def set_matrix(self, new_maze):
        self._maze = new_maze

    # -----------------------------------------------------------------------------------------------
    ##
    def show_solution(self, sol_set):
        """
        Show result of the solution path in the form of graph.
        Different color represents different states(free or blocked or passed).
        """
        new_matrix = copy.deepcopy(self._maze)
        path_value = 0.5
        if sol_set is None:
            return
        for sol in sol_set:
            new_matrix[sol[0]][sol[1]] = path_value
        plt.figure('Solution of maze with p=' + str(self._p))
        plt.imshow(new_matrix)
        plt.show()

    # -----------------------------------------------------------------------------------------------
    ##
    def get_actual_p(self):
        """
        :return: actual portion of the block cells in the maze
        """
        temp1 = sum(map(sum, self._maze))
        temp2= pow(self._dim, 2)
        # actual_p = temp1 / temp2
        actual_p = temp1
        return actual_p

