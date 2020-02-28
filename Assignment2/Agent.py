from grid import Grid
import random


class Agent:
    def __init__(self, grids, mines_num):
        self.grids = grids  # the play ground
        self.grids_dim = grids.dim  # dimension of the grids
        self.mines_num = mines_num  # total number of mines
        self.mines_left = mines_num     # number of hidden mines
        self.score = 0  # number of identified mines
        # a dict of points, the value of a point is a list which has 6 elements
        self.knowledge_base = {}    # 1. bool: is safe? 2. int: the clue 3. int: total neighbors
        # 4. int: safe neighbors 5. mine neighbors 6. hidden neighbors
        self.free_list = []     # a list of covered grids but identified safe
        self.mine_list = []     # a list to record identified mines
        self.covered_list = []  # a list of covered grids
        for i in range(self.grids_dim):
            for j in range(self.grids_dim):
                self.covered_list.append((i, j))
        random.shuffle(self.covered_list)   # simulate the random choose

    def random_choose(self):
        """
        function to randomly return a point to explore
        :return: coordinate of a point
        """
        if self.covered_list:
            return self.covered_list.pop()
        else:
            print("There is nowhere to go.")
            return None

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
                # if (x+i, y+j) in self.knowledge_base:
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
                if (x + i, y + j) in self.covered_list:
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
                    self.knowledge_base[(x + i, y + j)][3] += 1
                    self.knowledge_base[(x + i, y + j)][5] -= 1

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
                    self.knowledge_base[(x + i, y + j)][4] += 1
                    self.knowledge_base[(x + i, y + j)][5] -= 1

    def update_kb(self, cor, mines_num):
        """
        function to update knowledge base when a point is identified safe
        :param cor: the point
        :param mines_num: the clue, number of neighbor mines
        """
        if mines_num is None:
            mines_num = -1
        total_neighbors = self.grids.num_of_neighbors(cor)
        free_identified = self.get_safe_num(cor)
        mine_identified = self.get_mine_num(cor)
        hidden = self.get_hidden_num(cor)
        self.knowledge_base[cor] = \
            [True, mines_num, total_neighbors, free_identified, mine_identified, hidden]
        self.update_other_hidden(cor)
        self.infer(cor)

    def update_kb_free(self, cor, mines_num):
        """
        function to update knowledge base when a point is identified safe, but the point is
        from free list
        :param cor: the point
        :param mines_num: the clue, number of neighbor mines
        """
        if mines_num is None:
            mines_num = -1
        total_neighbors = self.grids.num_of_neighbors(cor)
        free_identified = self.get_safe_num(cor)
        mine_identified = self.get_mine_num(cor)
        hidden = self.get_hidden_num(cor)
        self.knowledge_base[cor] = \
            [True, mines_num, total_neighbors, free_identified, mine_identified, hidden]
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
                if (x + i, y + j) in self.covered_list and \
                        (x + i, y + j) not in self.free_list:
                    print("Detect free cell:", (x + i, y + j))
                    self.free_list.append((x + i, y + j))
                    self.covered_list.remove((x + i, y + j))
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
                if (x + i, y + j) in self.covered_list and \
                        (x + i, y + j) not in self.mine_list:
                    print("Detect a mine:", (x + i, y + j))
                    self.grids.flag_mine((x + i, y + j))
                    self.mine_list.append((x + i, y + j))
                    self.covered_list.remove((x + i, y + j))
                    changed_list.append((x + i, y + j))
                    self.score += 1
        return changed_list

    def lets_play(self):
        """
        main function to simulate the agent's move
        """
        # while len(self.mine_list) < self.mines_num:
        while self.covered_list:
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
        # while len(self.mine_list) < self.mines_num:
        while self.covered_list:
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
                self.mine_list.append(next_move)
                self.update_other_mine(next_move)
                self.infer(next_move)
        print("The agent completed the task!")
        print("Mines are:", self.mine_list)
        print("Score:", self.score/self.mines_num)
        return self.score/self.mines_num

    def lets_play_immortal_prob(self, p):
        """
        Main function to simulate the agent's move, but the agent won't die when discover
        a mine. When discover a grid, it has a probability p not showing the clue.
        :param p: the probability not showing the clue
        :return: the rate, number of identified mines/total number of mines
        """
        while self.covered_list:
            if self.free_list:
                next_move = self.free_list.pop()
                # result = self.grids.uncover_grid(next_move)
                result = self.grids.uncover_grid_probability(next_move, p)
                self.update_kb_free(next_move, result)
                continue
            else:
                next_move = self.random_choose()
            # result = self.grids.uncover_grid(next_move)
            result = self.grids.uncover_grid_probability(next_move, p)
            print("next move:", next_move, "result:", result)
            if result != -1:
                self.update_kb(next_move, result)
            else:
                print("BOOM! Detect a mine:", next_move)
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
    # avg += agent.lets_play_immortal_prob(0.1)
print("Average Score:", avg/1000)