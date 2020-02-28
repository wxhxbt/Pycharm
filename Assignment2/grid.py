import random


class Cell:
    def __init__(self, is_mine):
        """
        :param is_mine: true or false
        """
        self.isMine = is_mine
        self.isCovered = True
        if self.isMine is not True:
            self.numOfMines = 0
        else:
            self.numOfMines = -1
        self.isFlag = False
        self.neighbor = -1


class Grid:
    def __init__(self, dim, N):
        """
        :param dim: the dimension of map
        :param N: number of mines
        """
        self.dim = dim
        self.grid = [[] * dim for i in range(dim)]
        self.numOfMine = 0
        self.generate_grid(N)
        self.mark_mine_number()

    def get_cell(self, x, y):
        """
        :param x: x coordinate
        :param y: y coordinate
        :return: the value of cell
        """
        return self.grid[x][y]

    def generate_grid(self, N):
        """
        generate a grid using random.shuffle()
        :param N: the number of mines
        :return:
        """
        temp_list = []
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                cell = Cell(False)
                self.grid[i].append(cell)
                temp_list.append([cell, i, j])
                for ii in range(-1, 2):
                    for jj in range(-1, 2):
                        if 0 <= i + ii < self.dim and 0 <= j + jj < self.dim:
                            cell.neighbor += 1
        print(temp_list)
        random.shuffle(temp_list)
        print(temp_list)
        for i in range(0, N):
            self.grid[temp_list[i][1]][temp_list[i][2]] = Cell(True)

    def mark_mine_number(self):
        """
        mark the number of every cell
        :return:
        """
        for i in range(self.dim):
            for j in range(self.dim):
                cell = self.get_cell(i, j)
                for ii in range(-1, 2):
                    for jj in range(-1, 2):
                        if ii == 0 and jj == 0:
                            continue
                        if 0 <= i + ii <= self.dim - 1 and 0 <= j + jj <= self.dim - 1:
                            adj = self.get_cell(i + ii, j + jj)
                            if adj.isMine and not cell.isMine:
                                cell.numOfMines += 1

    def num_of_covered_cell(self, i, j):
        """
        mark the number of covered cell
        :param i: x coordinator
        :param j: y coordinator
        :return: the number of covered cell
        """
        result = 0
        for p in range(-1, 2):
            for q in range(-1, 2):
                cur_cell = self.get_cell(i + p, j + q)
                if cur_cell.isCovered and not cur_cell.isFlag:
                    result += 1
        return result

    def num_of_flags(self, i, j):
        """
        mark the number of flags
        :param i: x coordinator
        :param j: y coordinator
        :return: the number of covered cell
        """
        result = 0
        for p in range(-1, 2):
            for q in range(-1, 2):
                if p == 0 and q == 0:
                    continue
                cur_cell = self.get_cell(i + p, j + q)
                if cur_cell.isFlag:
                    result += 1
        return result

    def num_of_neighbors(self, cor):
        """
        return the number of neighbors
        :param i: x coordinator
        :param j: y coordinator
        :return: the number of neighbors
        """
        i, j = cor[0], cor[1]
        result = 0
        for p in range(-1, 2):
            for q in range(-1, 2):
                if p == 0 and q == 0:
                    continue
                if 0 <= i + p < self.dim and 0 <= j + q < self.dim:
                    result += 1
        return result

    def uncover_grid(self, cor):
        """
        return the number of every cell
        :param i: x coordinator
        :param j: y coordinator
        :return:
        """
        i, j = cor[0], cor[1]
        if self.grid[i][j].isMine is True:
            return -1
        else:
            return self.grid[i][j].numOfMines

    def uncover_grid_probability(self, cor, p):
        """
        return the number of every cell
        """
        i, j = cor[0], cor[1]
        random_num = random.random()
        if self.grid[i][j].isMine is True:
            return -1
        else:
            if random_num < p:
                return None
            else:
                return self.grid[i][j].numOfMines

    def flag_mine(self, cor):
        """
        flag a mine
        :param i: x coordinator
        :param j: y coordinator
        :return:
        """
        i, j = cor[0], cor[1]
        if self.uncover_grid(cor) == -1:
            self.grid[i][j].isFlag = True
            return True
        else:
            print("Wrong identification! That is not a mine.")
            return False
