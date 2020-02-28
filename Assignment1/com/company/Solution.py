from queue import Queue
import math


class Solution(object):
    # -----------------------------------------------------------------------------------------------
    #
    def __init__(self, maze):
        """
        :param maze: The matrix of maze we build
        """
        self._maze = maze

    # -----------------------------------------------------------------------------------------------
    #
    def is_restricted(self, a, b):
        """
        Judge whether the state is restricted or not.
        :param a: The x-coordinate of position
        :param b: The y-coordinate of position
        :return: Boolean
        """
        x, y = a, b
        if x < 0 or x >= len(self._maze) or y < 0 or y >= len(self._maze):
            return True
        elif self._maze[x][y] == 1:
            return True
        else:
            return False

    # -----------------------------------------------------------------------------------------------
    #
    def depth_first_search(self, start, goal):
        """
        The function of Depth First Search algorithm to find a path from begin to the end
        :param start: start point
        :param goal: end point
        :return: The list of solution.
        """
        # cur_pos = (0, 0)
        # goal = (len(self._maze) - 1, len(self._maze) - 1)
        cur_pos = start
        fringe = []     # The structure of fringe is a stack, LIFO
        closet = set()
        path_dict = {}  # Record the parent state of a current one
        solution = []
        fringe.append(cur_pos)
        path_dict[cur_pos] = None
        max_fringe, nodes_expanded = 1, 0

        while len(fringe) != 0:
            cur_pos = fringe.pop()
            nodes_expanded += 1
            if cur_pos not in closet:
                if cur_pos == goal:
                    # According to dictionary of path return the solution set
                    solution.append(cur_pos)
                    parent = path_dict.get(cur_pos)
                    while parent is not None:
                        solution.append(parent)
                        parent = path_dict.get(parent)
                    return solution, nodes_expanded, max_fringe
                # Expand children state of the current one
                x, y = cur_pos[0] + 1, cur_pos[1]
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.append((x, y))
                    path_dict[(x, y)] = cur_pos
                x, y = cur_pos[0] - 1, cur_pos[1]
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.append((x, y))
                    path_dict[(x, y)] = cur_pos
                x, y = cur_pos[0], cur_pos[1] + 1
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.append((x, y))
                    path_dict[(x, y)] = cur_pos
                x, y = cur_pos[0], cur_pos[1] - 1
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.append((x, y))
                    path_dict[(x, y)] = cur_pos
                closet.add(cur_pos)
                max_fringe = max(len(fringe), max_fringe)
        return None, nodes_expanded, max_fringe

    # -----------------------------------------------------------------------------------------------
    #
    def breadth_first_search(self, start, goal):
        """
        The function of Breadth First Search algorithm to find a path from begin to the end.
        The structure of this algorithm is basically the same as DFS except for the structure of fringe.
        :param start: start point
        :param goal: end point
        :return: The list of solution.
        """
        # cur_pos = (0, 0)
        # goal = (len(self._maze) - 1, len(self._maze) - 1)
        cur_pos = start
        fringe = Queue()    # The structure of fringe is a queue, FIFO
        closet = set()
        path_dict = {}
        solution = []
        fringe.put(cur_pos)
        path_dict[cur_pos] = None
        max_fringe, nodes_expanded = 1, 0

        while not fringe.empty():
            cur_pos = fringe.get()
            nodes_expanded += 1
            if cur_pos not in closet:
                if cur_pos == goal:
                    solution.append(cur_pos)
                    parent = path_dict.get(cur_pos)
                    while parent is not None:
                        solution.append(parent)
                        parent = path_dict.get(parent)
                    return solution, nodes_expanded, max_fringe
                x, y = cur_pos[0] + 1, cur_pos[1]
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.put((x, y))
                    path_dict[(x, y)] = cur_pos
                x, y = cur_pos[0] - 1, cur_pos[1]
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.put((x, y))
                    path_dict[(x, y)] = cur_pos
                x, y = cur_pos[0], cur_pos[1] + 1
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.put((x, y))
                    path_dict[(x, y)] = cur_pos
                x, y = cur_pos[0], cur_pos[1] - 1
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.put((x, y))
                    path_dict[(x, y)] = cur_pos
                max_fringe = max(fringe.qsize(), max_fringe)
                closet.add(cur_pos)
        return None, nodes_expanded, max_fringe

    # -----------------------------------------------------------------------------------------------
    #
    def bidirectional_breadth_first_search(self, start, goal):
        """
        The function of Bi-Directional Breadth First Search algorithm to find a path from begin to end.
        :param start: start point
        :param goal: end point
        :return: The list of solution.
        """
        left_start = start
        right_start = goal
        temp_x = int((goal[0] + 1) / 2)
        temp_y = int((goal[0] + 1) / 2)
        while self.is_restricted(temp_x, temp_y):
            temp_x -= 1
            temp_y -= 1
        temp_goal = (temp_x, temp_y)
        left_solution = self.breadth_first_search(left_start, temp_goal)[0]
        right_solution = self.breadth_first_search(right_start, temp_goal)[0]
        if left_solution and right_solution:
            left_solution.pop(0)
            right_solution = right_solution[::-1]
            solution = right_solution + left_solution
        else:
            solution = None
        return solution, 0, 0


# -----------------------------------------------------------------------------------------------
##
def astar_search(maze, dim, method):
    open_list = []
    close_list = set()
    fringe_ban = set()
    solution = []
    goal = (dim - 1, dim - 1)
    cur = ((0, 0), 0, h((0, 0), goal, method))
    path_dict = {cur: None}
    open_list.append(cur)

    max_fringe, nodes_expanded = 1, 0

    while len(open_list) > 0:
        cur = open_list.pop(0)
        nodes_expanded += 1
        # print(open_list)
        if cur[0] == goal:
            solution.append(cur[0])
            parent = path_dict.get(cur)
            while parent is not None:
                solution.append(parent[0])
                parent = path_dict.get(parent)
            return solution, nodes_expanded, max_fringe
        # throw away the path we just tested.
        # print(open_list)
        # insert children of path into open list. Each child is a path.
        for cell in adjacent_cells((cur[0], cur[1]), maze, goal, method):
            if cell[0] not in close_list and cell not in fringe_ban:
                fringe_ban.add(cell)
                temp = (cell[0], cell[1], cell[1] + h(cell[0], goal, method))
                path_dict[temp] = cur
                open_list = insert(temp, open_list)
        close_list.add(cur[0])  # and add its last cell to closed list
        max_fringe = max(len(open_list), max_fringe)
        # print(open_list)
    return None, nodes_expanded, max_fringe


# -----------------------------------------------------------------------------------------------
##
def adjacent_cells(destination, maze, goal, method):
    cells = []
    i, j = destination[0]
    newdes = destination[1]+1

    if i > 0:
        if maze[i - 1][j] != 1:
            cells += [((i - 1, j), newdes)]
    if j > 0:
        if maze[i][j - 1] != 1:
            cells += [((i, j - 1), newdes)]
    if i < len(maze) - 1:
        if maze[i + 1][j] != 1:
            cells += [((i + 1, j), newdes)]
    if j < len(maze) - 1:
        if maze[i][j + 1] != 1:
            cells += [((i, j + 1), newdes)]

    # print("Adjacent Cells: ", cells)
    return cells


# insert: path * list<path>  * cell -> list<path>
# If p is a path, L is a list of paths sorted in nondecreasing order
# by estimated total cost, and c is a cell, then insert(p,L,c) is the list
# obtained from L by inserting p so that the list remains sorted.
# The estimated total cost of a path is its length plus the manhattan distance
# from its last cell to c. For extra credit, write this so that it runs in time
# O(log(len(L))).
def insert(cur, open_list):
    # The estimated total cost of a path is its length plus the manhattanD.
    # cost = length + manhattanD(?, cheesePosition)
    for i in range(len(open_list)):
        if cur[2] < open_list[i][2]:
            return open_list[0:i] + [cur] + open_list[i:len(open_list)]
    return open_list + [cur]


# ManhattanD: cell*cell -> int
# manhattanD(c1,c2) is the Manhattan distance between c1 and c2
def h(c1, c2, method):
    i1, j1 = c1
    i2, j2 = c2
    if method == "Euclid":
        return math.sqrt((i1 - i2) * (i1 - i2) + (j1 - j2) * (j1 - j2))
    if method == "Manhattan":
        return abs(i1 - i2) + abs(j1 - j2)
