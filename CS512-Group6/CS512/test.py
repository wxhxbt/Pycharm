from GeneticAlgorithm import GA
START_POINT = ''
STOP_POINTS = []

# data = {'A': (0, 0), 'B': (1, 0), 'C': (2, 0),
#         'D': (0, 1), 'E': (1, 1), 'F': (2, 1),
#         'G': (0, 2), 'H': (1, 2), 'I': (2, 2)}

class TSP:
    def __init__(self, data):
        self.data = data
        self.start = None
        self.stops = []

    def set_start(self, start):
        self.start = start

    def set_stops(self, stops):
        self.stops = stops


def data_load():
    data = {}
    with open('us48capitals.txt', 'r') as f:
        for line in f:
            lst = list(map(int, line.split(' ')))
            data[str(lst[0])] = (lst[1], lst[2])
    return data


def run_test():
    data = data_load()
    # input_stops = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    # start = 'A'
    input_stops = STOP_POINTS
    start = START_POINT
    tsp = TSP(data)
    tsp.set_start(start)
    tsp.set_stops(input_stops)
    approx_ga = GA(100, 0.1, tsp)
    # best = approx_ga.genetic_alg()
    best = approx_ga.genetic_alg_iteration_based()
    path = best[0]
    path.insert(0, start)
    path.insert(len(input_stops) + 1, start)
    print('path:', path, 'total distance:', approx_ga.compute_length(best[0]))
    return path
