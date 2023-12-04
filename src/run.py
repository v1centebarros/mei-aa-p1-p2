from collections import defaultdict

from algorithms import adaptive_randomized_vertex_cover, randomized_vertex_cover, greedy_vertex_cover, bruteforce
from utils import MAXIMUM_NUMBER_EDGES, NUMBER_OF_ITERATIONS, SEED, log
import pickle, os

graphs = pickle.load(open("../graphs/all_graphs.pickle", "rb"))


def run(algorithm, name):
    results = defaultdict(dict)
    for max_edges in MAXIMUM_NUMBER_EDGES:
        for size in range(4, 256):
            log.info(
                f"Running {name} algorithm for graph with size {size}, seed {SEED} and maximum number of edges {max_edges}")
            results[max_edges][size] = algorithm(graphs[max_edges][size])
            log.info(
                f"Finished running {name} algorithm for graph with size {size}, seed {SEED} and maximum number of edges {max_edges}")

    pickle.dump(results, open(f"../results/results_complete_{name}.pickle", "wb"))


def run_graph(algorithm, name, graph):
    log.info(
        f"Running {name} algorithm for graph with size {graph.number_of_nodes()}, maximum number of edges {graph.number_of_edges()}")
    result = algorithm(graph)
    log.info(
        f"Finished running {name} algorithm for graph with size {graph.number_of_nodes()}, seed {SEED} and maximum number of edges {graph.number_of_edges()}")
    pickle.dump(result, open(f"../results/results_{name}.pickle", "wb"))


def marathon():
    for algorithm, name in [(randomized_vertex_cover, "random_vertex_cover"),
                            (adaptive_randomized_vertex_cover, "adaptive_randomized_vertex_cover")]:
        for max_iterations in NUMBER_OF_ITERATIONS:
            results = defaultdict(dict)
            for max_edges in MAXIMUM_NUMBER_EDGES:
                for size in range(4, 256):
                    log.info(
                        f"Running adaptive randomized algorithm for graph with size {size}, seed {SEED} and maximum number of edges {max_edges}")
                    results[max_edges][size] = algorithm(graphs[max_edges][size], max_iterations)
                    log.info(
                        f"Finished running adaptive randomized algorithm for graph with size {size}, seed {SEED} and maximum number of edges {max_edges}")

            pickle.dump(results, open(f"../results/results_{name}_{max_iterations}.pickle", "wb"))


if __name__ == "__main__":
    marathon()
