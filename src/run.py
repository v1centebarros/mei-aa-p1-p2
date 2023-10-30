import argparse, logging
from collections import defaultdict

from utils import generate_random_graph
from algorithms import bruteforce, bruteforce_bitwise, greedy_vertex_cover
from utils import GRAPH_SIZES, MAXIMUM_NUMBER_EDGES, SEED, log
import pickle


def run():
    results = defaultdict(list)
    for size in GRAPH_SIZES:
            for max_edges in MAXIMUM_NUMBER_EDGES:
                log.info(f"Graf size: {size}, max_edges: {max_edges}")
                G = generate_random_graph(SEED, size, max_edges)
                log.info(f"Running Bruteforce size {size}, seed {SEED} and maximum number of edges {max_edges}")
                results['bruteforce'].append(bruteforce(G))
                log.info(f"Running Bruteforce Bitwise size {size}, seed {SEED} and maximum number of edges {max_edges}")
                results['bruteforce_bitwise'].append(bruteforce_bitwise(G))
                log.info(f"Running Greedy Vertex Cover size {size}, seed {SEED} and maximum number of edges {max_edges}")
                results['greedy_vertex_cover'].append(greedy_vertex_cover(G))
                log.info(f"Finished running algorithms for graph with size {size}, seed {SEED} and maximum number of edges {max_edges}")
            pickle.dump(results, open(f"../results/results_{size}.pickle", "wb"))
    

    

if __name__ == "__main__":
    run()