from time import time
import networkx as nx
import matplotlib.pyplot as plt

def generate_random_graph(seed, size):
    return nx.fast_gnp_random_graph(size, 0.8, seed=seed)

def draw_graph(graph):
    nx.draw(graph, with_labels=True)
    plt.show()



def time_algorithm(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()

        print("Time elapsed: ", end - start)
        print("Result: ", result)
        return result

    return wrapper