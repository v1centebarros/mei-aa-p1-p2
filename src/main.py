from utils import generate_random_graph, draw_graph
from algorithms import bruteforce, bruteforce_bitwise, greedy_vertex_cover

SEED = 97787




def main():
    G = generate_random_graph(SEED, 10)

    algoritms = [bruteforce, bruteforce_bitwise, greedy_vertex_cover]

    for algorithm in algoritms:
        algorithm(G)


if __name__ == "__main__":
    main()