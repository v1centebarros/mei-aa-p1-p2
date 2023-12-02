import json
from time import time
import networkx as nx
import matplotlib.pyplot as plt
from collections import namedtuple
import logging, pickle

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

MAXIMUM_NUMBER_EDGES = [0.125, 0.25, 0.5, 0.75]
SEED = 97787
SIZES = 256

Result = namedtuple('Result', ['function', 'result', 'operations', 'time', 'solution_counter'])


def generate_random_graph(seed=SEED, size=10, maximum_number_edges=0.8):
    return nx.fast_gnp_random_graph(size, maximum_number_edges, seed=seed)


def generate_all_graphs():
    all_graphs = {}
    for maximum_number_edges in MAXIMUM_NUMBER_EDGES:
        all_graphs[maximum_number_edges] = {}
        for size in range(1, SIZES):
            G = generate_random_graph(SEED, size, maximum_number_edges)
            all_graphs[maximum_number_edges][size] = G
    return all_graphs


def save_graphs():
    graphs = generate_all_graphs()
    pickle.dump(graphs, open("graphs/all_graphs.pickle", "wb"))


def draw_graph(graph):
    nx.draw(graph, with_labels=True)
    plt.show()


def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time()
        result, operations, solution_counter = func(*args, **kwargs)
        end = time()

        return Result(func.__name__, result, operations, end - start, solution_counter)

    return wrapper


def deprecated(func):
    def wrapper(*args, **kwargs):
        log.warning(f"{func.__name__} is deprecated")
        raise DeprecationWarning

    return wrapper


def import_data(file):
    return pickle.load(open(f"{file}", "rb"))


def convert_to_json(data, path):
    new_data = {}
    for size in data.keys():
        new_data[size] = {}
        for max_edges in data[size].keys():
            new_data[size][max_edges] = {}
            new_data[size][max_edges]["operations"] = data[size][max_edges].operations
            new_data[size][max_edges]["time"] = data[size][max_edges].time
            new_data[size][max_edges]["result"] = list(data[size][max_edges].result)
            new_data[size][max_edges]["solution_counter"] = data[size][max_edges].solution_counter

    json.dump(new_data, open(path, "w"), indent=4)


def validate_solution(graph, cover):
    for edge in graph.edges():
        if edge[0] not in cover and edge[1] not in cover:
            return False
    return True


def validate_all_solutions(graphs, data):
    for max_edges in MAXIMUM_NUMBER_EDGES:
        for size in range(4, 256):
            print(f"Solution: {data[max_edges][size].result}")
            print(f"Graph: {graphs[max_edges][size]}")
            if validate_solution(graphs[max_edges][size], data[max_edges][size].result):
                print(f"Valid solution for graph with size {size} and maximum number of edges {max_edges}")
            else:
                print(f"Invalid solution for graph with size {size} and maximum number of edges {max_edges}")


def read_graph_from_txt(filename):
    # Create an empty graph
    G = nx.Graph()

    with open(filename, 'r') as file:
        lines = file.readlines()

        # Skip the first three lines (headers/metadata)
        for line in lines[4:]:
            # Split the line into vertices and add an edge to the graph
            u, v = map(int, line.strip().split())
            G.add_edge(u, v)
    return G


if __name__ == "__main__":
    big_graph = read_graph_from_txt("../graphs/SWlargeG.txt")
    print(big_graph.number_of_nodes())
    print(big_graph.number_of_edges())
    # save as pickle
    pickle.dump(big_graph, open("../graphs/big_graph.pickle", "wb"))
