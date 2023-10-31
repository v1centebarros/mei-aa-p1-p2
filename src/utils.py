from time import time
import networkx as nx
import matplotlib.pyplot as plt
from collections import namedtuple
import logging, pickle

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

MAXIMUM_NUMBER_EDGES = [0.125, 0.25, 0.5, 0.75]

GRAPH_SIZES = [10,50,100,200,300,400,500,600,700,800,900,1000]

SEED = 97787


Result = namedtuple('Result', ['function','result', 'operations','time'])


def generate_random_graph(seed=SEED, size=10, maximum_number_edges=0.8):
    return nx.fast_gnp_random_graph(size, maximum_number_edges, seed=seed)


def generate_all_graphs():
    all_graphs = {}
    for maximum_number_edges in MAXIMUM_NUMBER_EDGES:
        all_graphs[maximum_number_edges] = {}
        for size in range(1,29):
            G = generate_random_graph(SEED, size, maximum_number_edges)
            all_graphs[maximum_number_edges][size] = G
    return all_graphs


def save_graphs():
    graphs = generate_all_graphs()
    pickle.dump(graphs, open(f"results/all_graphs.pickle", "wb"))


def draw_graph(graph):
    nx.draw(graph, with_labels=True)
    plt.show()

def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time()
        result, operations = func(*args, **kwargs)
        end = time()

        return Result(func.__name__, result, operations, end - start)

    return wrapper
