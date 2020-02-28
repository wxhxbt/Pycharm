from grid import Grid
import random


class Agent:
    def __init__(self, grids, mines_num):
        # same as agent.py except a couple of attributes
        self.grids = grids
        self.grids_dim = grids.dim
        self.mines_num = mines_num
        self.mines_left = mines_num
        # the expectation of a grid that is not a neighbor of any point in knowledge base
        self.E_not_neighbor = mines_num/(grids.dim * grids.dim)
        self.score = 0
        self.knowledge_base = {}
        self.free_list = []
        self.mine_list = []
        self.covered_list = []      # it is a list recording the non-neighbor points now
        for i in range(self.grids_dim):
            for j in range(self.grids_dim):
                self.covered_list.append((i, j))
        random.shuffle(self.covered_list)
        self.covered_neighbor = {}  # it is a list recording neighbor points and the corresponding expectation

    def random_choose(self):
        """
        function to return a point which has the minimum expectation of being a mine
        :return: coordinates of the point
        """
        if self.covered_list:
            self.E_not_neighbor = self.mines_left/len(self.covered_list)
            min_e = self.E_not_neighbor
            for item in self.covered_neighbor:
                if self.covered_neighbor[item] < min_e:
                    min_e = self.covered_neighbor[item]
                    min_cor = item
            if min_e == self.E_not_neighbor:
                return self.covered_list.pop()
            else:
                del self.covered_neighbor[min_cor]
                return min_cor
        else:
            min_e = 9999.9
            for item in self.covered_neighbor:
                if self.covered_neighbor[item] < min_e:
                    min_e = self.covered_neighbor[item]
                    min_cor = item
            del self.covered_neighbor[min_cor]
            return min_cor

    def get_safe_num(self, cor):
        """
        compute the number of safe neighbor of a point
        :param cor: the point
        :return: the number of safe neighbor
        """
        num = 0
        x, y = cor[0], cor[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if (x+i, y+j) in self.free_list or (x+i, y+j) in self.knowledge_base:
                    num += 1
        return num

    def get_mine_num(self, cor):
        """
        compute the number of mine neighbor of a point
        :param cor: the point
        :return: the number of mine neighbor
        """
        num = 0
        x, y = cor[0], cor[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if (x+i, y+j) in self.mine_list:
                    num += 1
        return num

    def get_hidden_num(self, cor):
        """
        compute the number of hidden neighbor of a point
        :param cor: the point
        :return: the number of hidden neighbor
        """
        num = 0
        x, y = cor[0], cor[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                # if (x+i, y+j) in self.covered_list or (x+i, y+j) in self.free_list:
                if (x + i, y + j) in self.covered_list or (x + i, y + j) in self.covered_neighbor:
                    num += 1
        return num

    def update_other_hidden(self, cor):
        """
        function to update neighbors of a point which is identified safe
        :param cor: the point
        """
        x, y = cor[0], cor[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if (x+i, y+j) in self.knowledge_base:
                    t_m = self.knowledge_base[(x + i, y + j)][1]
                    i_m = self.knowledge_base[(x + i, y + j)][4]
                    hidden = self.knowledge_base[(x + i, y + j)][5]
                    self.update_candidates((x+i, y+j), t_m - i_m, hidden, -1)
                    self.knowledge_base[(x + i, y + j)][3] += 1
                    self.knowledge_base[(x + i, y + j)][5] -= 1
                    self.update_candidates((x+i, y+j), t_m - i_m, hidden - 1, 1)

    def update_other_mine(self, cor):
        """
        function to update neighbors of a point which is identified as a mine
        :param cor: the point
        """
        x, y = cor[0], cor[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if (x+i, y+j) in self.knowledge_base:
                    t_m = self.knowledge_base[(x + i, y + j)][1]
                    i_m = self.knowledge_base[(x + i, y + j)][4]
                    hidden = self.knowledge_base[(x + i, y + j)][5]
                    self.update_candidates((x + i, y + j), t_m - i_m, hidden, -1)
                    self.knowledge_base[(x + i, y + j)][4] += 1
                    self.knowledge_base[(x + i, y + j)][5] -= 1
                    self.update_candidates((x + i, y + j), t_m - i_m - 1, hidden - 1, 1)

    def update_kb(self, cor, mines_num):
        """
        function to update knowledge base when a point is identified safe
        :param cor: the point
        :param mines_num: the clue, number of neighbor mines
        """
        total_neighbors = self.grids.num_of_neighbors(cor)
        free_identified = self.get_safe_num(cor)
        mine_identified = self.get_mine_num(cor)
        hidden = self.get_hidden_num(cor)
        self.knowledge_base[cor] = \
            [True, mines_num, total_neighbors, free_identified, mine_identified, hidden]
        self.update_candidates(cor, mines_num - mine_identified, hidden, 1)
        self.update_other_hidden(cor)
        self.infer(cor)

    def update_candidates(self, cor, left_mines, hidden, p_or_m):
        """
        function to update the expectation of covered grids around a point
        :param cor: the point
        :param left_mines: total mines - identified mines
        :param hidden: hidden neighbors of the point
        :param p_or_m: determine +/- expectation
        """
        x, y = cor[0], cor[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if (x+i, y+j) in self.covered_list:
                    self.covered_list.remove((x+i, y+j))
                    self.covered_neighbor[(x+i, y+j)] = left_mines/hidden
                elif (x+i, y+j) in self.covered_neighbor:
                    self.covered_neighbor[(x+i, y+j)] += p_or_m * left_mines/hidden

    def update_kb_free(self, cor, mines_num):
        """
        function to update knowledge base when a point is identified safe, but the point is
        from free list
        :param cor: the point
        :param mines_num: the clue, number of neighbor mines
        """
        total_neighbors = self.grids.num_of_neighbors(cor)
        free_identified = self.get_safe_num(cor)
        mine_identified = self.get_mine_num(cor)
        hidden = self.get_hidden_num(cor)
        self.knowledge_base[cor] = \
            [True, mines_num, total_neighbors, free_identified, mine_identified, hidden]
        self.update_candidates(cor, mines_num-mine_identified, hidden, 1)
        self.infer(cor)

    def infer(self, cor):
        """
        function to infer new knowledge based on knowledge base
        :param cor: the point
        """
        x, y = cor[0], cor[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x + i, y + j) in self.knowledge_base:
                    kb_grid = self.knowledge_base[(x+i, y+j)]
                    if kb_grid[5] > 0:
                        if kb_grid[1] - kb_grid[4] == kb_grid[5]:
                            print("currently visit:", (x + i, y + j))
                            print("clue:", kb_grid[1], "mine:", kb_grid[4], "hidden:", kb_grid[5])
                            wait_inferred = self.add_mine((x+i, y+j))
                            for item in wait_inferred:
                                self.update_other_mine(item)
                                self.infer(item)
                        if kb_grid[2] - kb_grid[1] - kb_grid[3] == kb_grid[5]:
                            print("currently visit:", (x+i, y+j))
                            print("total:", kb_grid[2], "clue:", kb_grid[1], "safe:", kb_grid[3], "hidden:", kb_grid[5])
                            # self.add_safe((x+i, y+j))
                            wait_inferred = self.add_safe((x + i, y + j))
                            for item in wait_inferred:
                                self.update_other_hidden(item)
                                self.infer(item)

    def add_safe(self, cor):
        """
        Add the hidden neighbor of a point to free_list based on inference
        :param cor: the point
        :return: a list recording coordinates of safe points
        """
        changed_list = []
        x, y = cor[0], cor[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if (x + i, y + j) in self.covered_neighbor and \
                        (x + i, y + j) not in self.free_list:
                    print("Detect free cell:", (x + i, y + j))
                    self.free_list.append((x + i, y + j))
                    # self.covered_list.remove((x + i, y + j))
                    del self.covered_neighbor[(x+i, y+j)]
                    changed_list.append((x + i, y + j))
        return changed_list

    def add_mine(self, cor):
        """
        Add the hidden neighbor of a point to mine_list based on inference
        :param cor: the point
        :return: a list recording coordinates of mines
        """
        changed_list = []
        x, y = cor[0], cor[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if (x + i, y + j) in self.covered_neighbor and \
                        (x + i, y + j) not in self.mine_list:
                    print("Detect a mine:", (x + i, y + j))
                    self.grids.flag_mine((x + i, y + j))
                    self.mine_list.append((x + i, y + j))
                    # self.covered_list.remove((x + i, y + j))
                    del self.covered_neighbor[(x + i, y + j)]
                    changed_list.append((x + i, y + j))
                    self.mines_left -= 1
                    self.score += 1
        return changed_list

    def lets_play(self):
        """
        main function to simulate the agent's move
        """
        while self.mines_left > 0:
            if self.free_list:
                next_move = self.free_list.pop()
                result = self.grids.uncover_grid(next_move)
                self.update_kb_free(next_move, result)
                continue
            else:
                next_move = self.random_choose()
            result = self.grids.uncover_grid(next_move)
            print("next move:", next_move, "result:", result)
            if result != -1:
                self.update_kb(next_move, result)
            else:
                print("BOOM! Game Over. Score:", len(self.mine_list))
                exit()
        print("The agent has discovered all the mines!")
        print(self.mine_list)

    def lets_play_immortal(self):
        """
        main function to simulate the agent's move, but the agent won't die when discover
        a mine
        :return: the rate, number of identified mines/total number of mines
        """
        while self.mines_left > 0:
            if self.free_list:
                next_move = self.free_list.pop()
                result = self.grids.uncover_grid(next_move)
                self.update_kb_free(next_move, result)
                continue
            else:
                next_move = self.random_choose()
            result = self.grids.uncover_grid(next_move)
            print("next move:", next_move, "result:", result)
            if result != -1:
                self.update_kb(next_move, result)
            else:
                print("BOOM! Detect a mine:", next_move)
                self.mines_left -= 1
                self.mine_list.append(next_move)
                self.update_other_mine(next_move)
                self.infer(next_move)
        print("The agent completed the task!")
        print("Mines are:", self.mine_list)
        print("Score:", self.score/self.mines_num)
        return self.score/self.mines_num


# test code
avg = 0.0
for i in range(1000):
    DIM = 10
    test_grid = Grid(DIM, 20)
    # for ii in range(0, DIM):
    #     for jj in range(0, DIM):
    #         if test_grid.uncover_grid((ii, jj)) == -1:
    #             print(9, end=" ")
    #         else:
    #             print(test_grid.uncover_grid((ii, jj)), end=" ")
    #     print()
    # print(test_grid.num_of_neighbors((0,29)))
    agent = Agent(test_grid, 20)
    # agent.lets_play()
    avg += agent.lets_play_immortal()
print("Average Score:", avg/1000)