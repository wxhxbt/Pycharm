from com.company.Maze import *
from com.company.Solution import *
from random import randrange, random
import copy


def fitness(spl, ne, mfs):
    # a, b, c = 0, 0, 1
    # a, b, c = 1, 0, 0
    a, b, c = 0, 1, 0
    return int(a*spl + b*ne + c*mfs)


def initial_population(num, dim, p):
    population = []
    while len(population) < num:
        # p may be set random
        maze = Maze(dim, p)
        maze.build_maze()
        maze_matrix = maze.get_matrix()
        sol = Solution(maze_matrix)
        # params = sol.breadth_first_search((0, 0), (dim-1, dim-1))
        # params = sol.depth_first_search((0, 0), (dim - 1, dim - 1))
        params = astar_search(maze_matrix, dim, "Manhattan")
        if params[0] is not None:
            fit = fitness(len(params[0]), params[1], params[2])
        else:
            continue
        population.append((maze_matrix, fit))
    population.sort(key=(lambda x: x[1]), reverse=True)
    return population


def selection(population):
    # popu.COPY
    chosen = []
    category = [population[0][1]]
    for i in range(1, len(population)):
        category.append(category[i-1]+population[i][1])
    rand = randrange(category[-1])
    for i in range(len(category)):
        if rand < category[i]:
            chosen.append(population[i])
            population.pop(i)
            category = category[0:i]
            for j in range(i, len(population)):
                if category:
                    category.append(category[j-1]+population[j][1])
                else:
                    category.append(population[0][1])
            break
    rand = randrange(category[-1])
    for i in range(len(category)):
        if rand < category[i]:
            chosen.append(population[i])
            break
    return chosen


def get_children(nums, dim, population, p_m1, p_m2):
    children = []
    while len(children) < nums:
        rand = randrange(1, dim - 1)
        sel = selection(population.copy())
        m1 = sel[0][0]
        m2 = sel[1][0]
        co1 = m1[0:rand] + m2[rand:dim]
        co2 = m2[0:rand] + m1[rand:dim]
        c1 = mutation(copy.deepcopy(co1), p_m1, p_m2)
        c2 = mutation(copy.deepcopy(co2), p_m1, p_m2)
        solution1 = Solution(c1)
        # params1 = solution1.breadth_first_search((0, 0), (dim - 1, dim - 1))
        # params1 = solution1.depth_first_search((0, 0), (dim-1, dim-1))
        params1 = astar_search(c1, dim, "Manhattan")
        solution2 = Solution(c2)
        # params2 = solution2.breadth_first_search((0, 0), (dim - 1, dim - 1))
        # params2 = solution2.depth_first_search((0, 0), (dim-1, dim-1))
        params2 = astar_search(c2, dim, "Manhattan")
        if params1[0] is not None:
            fit1 = fitness(len(params1[0]), params1[1], params1[2])
            children.append((c1, fit1))
        if params2[0] is not None:
            fit2 = fitness(len(params2[0]), params2[1], params2[2])
            children.append((c2, fit2))
    children.sort(key=(lambda x: x[1]), reverse=True)
    return children


def difference(old_set, new_set):
    n1, n2 = 0, 0
    for i in range(len(old_set)):
        n1 += old_set[i][1]
        n2 += new_set[i][1]
    return n2 - n1


def mutation(maze, p1, p2):
    rand = random()
    dim = len(maze)
    ran_x = randrange(dim)
    ran_y = randrange(dim)
    if rand < p1:
        # print("Mutation1 occurred!")
        ran_p_m = random()
        if ran_p_m < 0.5:
            while maze[ran_x][ran_y] == 1 or (ran_x == 0 and ran_y == 0) or (ran_x == dim-1 and ran_y == dim-1):
                ran_x = randrange(dim)
                ran_y = randrange(dim)
            maze[ran_x][ran_y] = 1
        else:
            while maze[ran_x][ran_y] == 0:
                ran_x = randrange(dim)
                ran_y = randrange(dim)
            maze[ran_x][ran_y] = 0
    elif rand < p1+p2:
        # print("Mutation2 occurred!")
        while maze[ran_x][ran_y] == 0:
            ran_x = randrange(dim)
            ran_y = randrange(dim)
        rand_new_y = randrange(dim)
        while rand_new_y == ran_y or (ran_x == 0 and rand_new_y == 0) or (ran_x == dim-1 and rand_new_y == dim-1):
            rand_new_y = randrange(dim)
        maze[ran_x][ran_y] = 0
        maze[ran_x][rand_new_y] = 1
    return maze


def generate_hard_maze(nums, dim, p, p_m1, p_m2):
    population = initial_population(nums, dim, p)
    children = get_children(nums, dim, population.copy(), p_m1, p_m2)
    children = population + children
    children.sort(key=(lambda x: x[1]), reverse=True)
    children = children[0:nums]
    dif = difference(population, children)
    while dif > 10:
        population = children
        children = get_children(nums, dim, population.copy(), p_m1, p_m2)
        children = population + children
        children.sort(key=(lambda x: x[1]), reverse=True)
        children = children[0:nums]
        dif = difference(population, children)
        print(dif)
        print("Hardest maze:", children[0][1])
    return children[0]

