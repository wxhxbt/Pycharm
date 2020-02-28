from random import random, randint, shuffle
import matplotlib.pyplot as plt
from queue import Queue
import numpy as np


class Solution:
    def __init__(self, s_loc=None, d1_loc=None, d2_loc=None):
        self.size = 8
        if s_loc is not None and d1_loc is not None and d2_loc is not None:
            self.sheep = s_loc
            self.dog1 = d1_loc
            self.dog2 = d2_loc
        else:
            shuf = []
            for i in range(self.size):
                for j in range(self.size):
                    shuf.append((i, j))
            shuffle(shuf)
            self.sheep = shuf[0]
            self.dog1 = shuf[1]
            self.dog2 = shuf[2]

    def bfs(self, start, goal):
        cur_pos = start
        fringe = Queue()  # The structure of fringe is a queue, FIFO
        closet = set()
        path_dict = {}
        solution = []
        fringe.put(cur_pos)
        path_dict[cur_pos] = None

        while not fringe.empty():
            cur_pos = fringe.get()
            if cur_pos not in closet:
                if cur_pos == goal:
                    solution.append(cur_pos)
                    parent = path_dict.get(cur_pos)
                    while parent is not None:
                        solution.append(parent)
                        parent = path_dict.get(parent)
                    return solution
                x, y = cur_pos[0], cur_pos[1] + 1
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.put((x, y))
                    path_dict[(x, y)] = cur_pos
                x, y = cur_pos[0], cur_pos[1] - 1
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.put((x, y))
                    path_dict[(x, y)] = cur_pos
                x, y = cur_pos[0] + 1, cur_pos[1]
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.put((x, y))
                    path_dict[(x, y)] = cur_pos
                x, y = cur_pos[0] - 1, cur_pos[1]
                if self.is_restricted(x, y) is False and (x, y) not in closet:
                    fringe.put((x, y))
                    path_dict[(x, y)] = cur_pos

                closet.add(cur_pos)
        return None

    def bfs_left_priority(self, start, goal):
        cur_pos = start
        fringe = Queue()  # The structure of fringe is a queue, FIFO
        closet = set()
        path_dict = {}
        solution = []
        fringe.put(cur_pos)
        path_dict[cur_pos] = None

        while not fringe.empty():
            cur_pos = fringe.get()
            if cur_pos not in closet:
                if cur_pos == goal:
                    solution.append(cur_pos)
                    parent = path_dict.get(cur_pos)
                    while parent is not None:
                        solution.append(parent)
                        parent = path_dict.get(parent)
                    return solution
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

                closet.add(cur_pos)
        return None

    def is_restricted(self, a, b):
        x, y = a, b
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return True
        elif (x, y) == self.sheep:
            return True
        else:
            return False

    def get_goal(self):
        goal1 = (self.sheep[0], self.sheep[1] + 1)
        goal2 = (self.sheep[0] + 1, self.sheep[1])
        if self.sheep == (self.size - 1, self.size - 1):
            goal1 = (self.sheep[0] - 2, self.sheep[1])
            goal2 = (self.sheep[0], self.sheep[1] - 1)
        elif self.sheep == (0, self.size - 1):
            goal1 = (self.sheep[0], self.sheep[1] - 2)
        elif self.sheep == (self.size - 1, 0):
            goal2 = (self.sheep[0] - 2, self.sheep[1])
        elif self.sheep[0] == self.size - 1:
            goal2 = (self.sheep[0], self.sheep[1] - 1)
        elif self.sheep[1] == self.size - 1:
            goal1 = (self.sheep[0] - 1, self.sheep[1])

        return goal1, goal2

    def move_dogs(self):
        ori_dog1 = self.dog1
        ori_dog2 = self.dog2
        goal1, goal2 = self.get_goal()
        if goal1 != self.dog1:
            path1 = self.bfs(self.dog1, goal1)
            self.dog1 = path1[-2]
        if goal2 != self.dog2:
            if self.sheep[1] != 0:
                path2 = self.bfs(self.dog2, goal2)
            else:
                path2 = self.bfs_left_priority(self.dog2, goal2)
            self.dog2 = path2[-2]
        if self.dog1 == self.dog2:
            if self.dog1 == ori_dog1:
                self.dog2 = ori_dog2
            else:
                self.dog1 = ori_dog1

    def move_sheep(self):
        ava_loc = self.available_pos()
        if len(ava_loc) > 1:
            rand = randint(0, len(ava_loc) - 1)
            self.sheep = ava_loc[rand]
        elif len(ava_loc) == 1:
            self.sheep = ava_loc[0]
        else:
            pass

    def available_pos(self):
        pos = [(self.sheep[0] - 1, self.sheep[1]), (self.sheep[0] + 1, self.sheep[1]),
               (self.sheep[0], self.sheep[1] - 1), (self.sheep[0], self.sheep[1] + 1)]
        pos_copy = pos.copy()
        for loc in pos_copy:
            if self.is_restricted(loc[0], loc[1]) \
                    or loc == self.dog1 or loc == self.dog2:
                pos.remove(loc)
        return pos

    def is_over(self):
        if self.sheep == (0, 0) and self.dog1 == (0, 1) and self.dog2 == (1, 0):
            return True
        else:
            return False

    def show(self, sol = None):
        board = np.zeros((8, 8), dtype=np.int8)
        if sol is not None:
            for step in sol:
                board[step[0], step[1]] = 1
        board[self.sheep[0], self.sheep[1]] = 2
        board[self.dog1[0], self.dog1[1]] = 3
        board[self.dog2[0], self.dog2[1]] = 4
        plt.figure('Graph')
        plt.imshow(board)
        plt.show()

    def get_initial(self):
        return self.sheep, self.dog1, self.dog2


itr = 0
maxt = 0
total = 0
while itr < 1000:
    # sol = Solution((4, 0), (6, 3), (0, 7))
    sol = Solution()
    ini = sol.get_initial()
    time = 0
    # sol.show()
    while not sol.is_over():
        # sol.show()
        sol.move_dogs()
        sol.move_sheep()
        # print(sol.sheep, sol.dog1, sol.dog2)
        time += 1
    # print("Success! Times:", time)
    if time > maxt:
        maxt = time
        opt_ini = ini
    total += time
    itr += 1
print("optimal position:", opt_ini)
print("Max times:", maxt)
print("Average times:", total/1000)

# sol = Solution((4, 0), (6, 3), (0, 7))
# ini = sol.get_initial()
# time = 0
# # sol.show()
# while not sol.is_over():
#     # sol.show()
#     sol.move_dogs()
#     sol.move_sheep()
#     # print(sol.sheep, sol.dog1, sol.dog2)
#     time += 1
# print("Success! Times:", time)