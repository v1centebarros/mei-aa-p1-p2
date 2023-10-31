from collections import defaultdict

from algorithms import bruteforce, bruteforce_bitwise, greedy_vertex_cover
from utils import MAXIMUM_NUMBER_EDGES, SEED, log
import pickle

graphs = pickle.load(open(f"results/all_graphs.pickle", "rb"))

def run(algorithm,name):
    results = defaultdict(dict)
    for max_edges in MAXIMUM_NUMBER_EDGES:
        for size in range (1,29):
            log.info(f"Running {name} algorithm for graph with size {size}, seed {SEED} and maximum number of edges {max_edges}")
            results[max_edges][size] = algorithm(graphs[max_edges][size])
            log.info(f"Finished running {name} algorithm for graph with size {size}, seed {SEED} and maximum number of edges {max_edges}")
    
    pickle.dump(results, open(f"results/results_complete_{name}.pickle", "wb"))
   

if __name__ == "__main__":
    run(bruteforce,"bruteforce")