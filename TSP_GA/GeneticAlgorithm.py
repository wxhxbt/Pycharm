from random import randrange, random, shuffle
from copy import deepcopy
import math


class GA:
    def __init__(self, size, p, tsp):
        self.tsp = tsp
        self.size = size
        self.mutation_rate = p
        self.iteration = 1000

    def genetic_alg(self):
        population = self.initial_population()
        children = self.get_children(population.copy())
        children = population + children
        children.sort(key=(lambda x: x[1]), reverse=True)
        children = children[0:self.size]
        dif = self.difference(population, children)
        while dif > 10:
            population = children
            children = self.get_children(population.copy())
            children = population + children
            children.sort(key=(lambda x: x[1]), reverse=True)
            children = children[0:self.size]
            dif = self.difference(population, children)
            print(dif)
        return children[0]

    def genetic_alg_iteration_based(self):
        population = self.initial_population()
        children = self.get_children(population.copy())
        children = population + children
        children.sort(key=(lambda x: x[1]), reverse=True)
        children = children[0:self.size]
        for i in range(self.iteration):
            population = children
            children = self.get_children(population.copy())
            children = population + children
            children.sort(key=(lambda x: x[1]), reverse=True)
            children = children[0:self.size]
            if i % 100 == 0:
                print("iteration", i, ' path:', children[0][0])
                print("distance:", self.compute_length(children[0][0]))
        return children[0]

    def fitness(self, target):
        start = self.tsp.start
        total_dist = 0
        total_dist += math.sqrt(pow(self.tsp.data[start][0] - self.tsp.data[target[0]][0], 2) + \
                      pow(self.tsp.data[start][1] - self.tsp.data[target[0]][1], 2))
        for i in range(len(target) - 1):
            former = target[i]
            latter = target[i + 1]
            dist = math.sqrt(pow(self.tsp.data[former][0] - self.tsp.data[latter][0], 2) + \
                   pow(self.tsp.data[former][1] - self.tsp.data[latter][1], 2))
            total_dist += dist
        total_dist += math.sqrt(pow(self.tsp.data[target[-1]][0] - self.tsp.data[start][0], 2) + \
                      pow(self.tsp.data[target[-1]][1] - self.tsp.data[start][1], 2))
        return 100000 / total_dist

    def compute_length(self, target):
        start = self.tsp.start
        total_dist = 0
        total_dist += math.sqrt(pow(self.tsp.data[start][0] - self.tsp.data[target[0]][0], 2) + \
                      pow(self.tsp.data[start][1] - self.tsp.data[target[0]][1], 2))
        for i in range(len(target) - 1):
            former = target[i]
            latter = target[i + 1]
            dist = math.sqrt(pow(self.tsp.data[former][0] - self.tsp.data[latter][0], 2) + \
                   pow(self.tsp.data[former][1] - self.tsp.data[latter][1], 2))
            total_dist += dist
        total_dist += math.sqrt(pow(self.tsp.data[target[-1]][0] - self.tsp.data[start][0], 2) + \
                      pow(self.tsp.data[target[-1]][1] - self.tsp.data[start][1], 2))
        return total_dist

    def initial_population(self):
        population = []
        for i in range(self.size):
            single = self.tsp.stops.copy()
            shuffle(single)
            fit = self.fitness(single)
            population.append((single, fit))
        population.sort(key=(lambda x: x[1]), reverse=True)
        return population

    def selection(self, population):
        chosen = []
        for k in range(2):
            total_fit = 0
            for i in range(len(population)):
                total_fit += population[i][1]
            category = [population[0][1] / total_fit]
            for i in range(1, len(population)):
                category.append(category[i - 1] + population[i][1] / total_fit)
            rand = random()
            for i in range(len(category)):
                if rand < category[i]:
                    chosen.append(population[i])
                    population.pop(i)
                    break
        return chosen

    def get_children(self, population):
        children = []
        while len(children) < self.size:
            parent1, parent2 = self.selection(deepcopy(population))
            pos1 = randrange(0, len(parent1))
            pos2 = randrange(0, len(parent1))
            start = min(pos1, pos2)
            end = max(pos1, pos2)
            child1_p1, child1_p2, child2_p1, child2_p2 = [], [], [], []
            for i in range(start, end):
                child1_p1.append(parent1[0][i])
                child2_p1.append(parent2[0][i])
            for gene in parent2[0]:
                if gene not in child1_p1:
                    child1_p2.append(gene)
            for gene in parent1[0]:
                if gene not in child2_p1:
                    child2_p2.append(gene)
            child1 = child1_p1 + child1_p2
            child2 = child2_p1 + child2_p2
            child1_mut = self.mutation(deepcopy(child1))
            child2_mut = self.mutation(deepcopy(child2))
            fit1 = self.fitness(child1_mut)
            fit2 = self.fitness(child2_mut)
            children.append((child1_mut, fit1))
            children.append((child2_mut, fit2))
        children.sort(key=(lambda x: x[1]), reverse=True)
        return children

    def difference(self, old_set, new_set):
        n1, n2 = 0, 0
        for i in range(len(old_set)):
            n1 += old_set[i][1]
            n2 += new_set[i][1]
        return n2 - n1

    def mutation(self, target):
        rand = random()
        if rand < self.mutation_rate:
            pos1 = randrange(0, len(target) - 1)
            pos2 = randrange(0, len(target) - 1)
            temp = target[pos1]
            target[pos1] = target[pos2]
            target[pos2] = temp
        return target
