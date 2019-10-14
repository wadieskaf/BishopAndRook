import numpy as np
import random


class Population(object):
    mutation = 0.3
    population_list = []
    fitness_list = []
    pop_size = 0
    board_size = 0

    def __init__(self, pop_size, board_size):
        self.pop_size = pop_size
        self.board_size = board_size
        self.population_list = []

    def check_duplicate(self, array, j, comp):
        for k in range(0, j):
            temp = array[k, :]
            if np.array_equal(temp, comp):
                return True

        return False

    def check_duplicate_2(self, x, y):
        for k in range(0, self.board_size - 1):
            if np.array_equal(x, y[k, :]):
                return True
        return False

    def check_duplicate_3(self, x, y):
        for k in range(1, self.board_size):
            if np.array_equal(x, y[k, :]):
                return True
        return False

    def insert(self, x, y, z):

        self.population_list[x][0, 0] = y
        self.population_list[x][0, 1] = z

    def gen_population(self):
        self.population_list = []
        for i in range(0, self.pop_size):
            pop = np.zeros((self.board_size, 2), dtype=int)
            for j in range(0, self.board_size):
                x = random.randint(0, self.board_size - 1)
                y = random.randint(0, self.board_size - 1)
                if j == 0:
                    pop[j, 0] = x
                    pop[j, 1] = y
                else:
                    comp = np.array((x, y), dtype=int)
                    # print('j=', j)
                    # print('comp=')
                    # with fullprint():
                    #    print(comp)
                    while self.check_duplicate(pop, j, comp):
                        x = random.randint(0, self.board_size - 1)
                        y = random.randint(0, self.board_size - 1)
                        comp = np.array((x, y), dtype=int)

                    pop[j, 0] = x
                    pop[j, 1] = y
            self.population_list.append(pop)

    def print_pop(self):
        for i in range(0, self.pop_size):
            with fullprint():
                print(self.population_list[i])

    def print_chromosome(self, i):
        with fullprint():
            print(self.population_list[i])

    def check_conflict_1(self, k, i, j):
        x = self.population_list[k][i, 0] - self.population_list[k][j, 0]
        y = self.population_list[k][i, 1] - self.population_list[k][j, 1]
        if x == y or x == -y:
            return int(1)
        else:
            return int(0)

    def check_conflict_2(self, k, i, j):
        if (self.population_list[k][i, 0] == self.population_list[k][j, 0] or self.population_list[k][i, 1] ==
                self.population_list[k][j, 1]):

            return int(1)
        else:
            return int(0)

    def calculate_fitness(self):
        for k in range(0, self.pop_size):
            num_of_conflicts = 0
            for i in range(0, self.board_size // 2):
                for j in range(i + 1, self.board_size):
                    num_of_conflicts += self.check_conflict_1(k, i, j)
            for i in range(self.board_size // 2, self.board_size):
                for j in range(0, self.board_size // 2):
                    num_of_conflicts += self.check_conflict_2(k, i, j)
                for j in range(i + 1, self.board_size):
                    num_of_conflicts += self.check_conflict_2(k, i, j)
            self.fitness_list.append(num_of_conflicts)

    def crossover(self, x, y):
        temp = x[3, :]
        x[3, :] = y[3, :]
        y[3, :] = temp

    def gen_next_population(self):
        next_gen_list = []
        i = 0
        while i < self.pop_size:
            x = random.randint(0, self.pop_size - 1)
            y = random.randint(0, self.pop_size - 1)
            c1 = self.population_list[x]
            c2 = self.population_list[y]
            luck = random.uniform(0, 1)
            if luck > self.mutation:
                while self.check_duplicate_2(c1[3, :], c2) or self.check_duplicate_2(c2[3, 1], c1) or y == x:
                    y = random.randint(0, self.pop_size - 1)
                    c2 = self.population_list[y]
                self.crossover(c1, c2)
                next_gen_list.append(c1)
                next_gen_list.append(c2)
                i += 2
            else:
                # print('mutant happened')
                m = random.randint(0, self.board_size - 1)
                n = random.randint(0, self.board_size - 1)
                ar = np.array((m, n), dtype=int)
                # print(ar)
                while self.check_duplicate_3(ar, self.population_list[x]):
                    m = random.randint(0, self.board_size - 1)
                    n = random.randint(0, self.board_size - 1)
                    ar = np.array((m, n), dtype=int)
                    # print(ar)
                self.insert(x, m, n)
        self.population_list = next_gen_list
        self.fitness_list = []
        self.calculate_fitness()

    def find_optimal_solution(self):
        gen = 1
        t = 0 in self.fitness_list
        while not t:
            gen += 1
            #print('gen = ', gen)
            self.gen_next_population()
            t = 0 in self.fitness_list
        i = self.fitness_list.index(0)
        print('optimal solution')
        # print('final gen = ', gen)
        # self.print_chromosome(i)
        print(self.population_list[i])


p = Population(100, 4)
p.gen_population()
p.calculate_fitness()
p.find_optimal_solution()
