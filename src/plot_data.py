from pprint import pprint

from matplotlib import pyplot as plt
from utils import MAXIMUM_NUMBER_EDGES, import_data


def plot_number_operations_vs_number_of_vertices(results, name, log=False, save=False, show=False):
    for max_edges in MAXIMUM_NUMBER_EDGES:
        x = []
        y = []
        for size in range(4, 29):
            x.append(size)
            y.append(results[max_edges][size].operations)
        if log:
            plt.semilogy(x, y, label=f"edges ratio: {max_edges}")
        else:
            plt.plot(x, y, label=f"edges ratio: {max_edges}")
        plt.xlabel("Number of vertices")
        plt.ylabel("Number of operations")
        plt.title(f"Number of operations vs number of vertices for {name} algorithm")
        plt.legend()

    if save:
        plt.savefig(f"../charts/{name}_number_operations_vs_number_of_vertices.png")
    if show:
        plt.show()

    plt.close()


def plot_time_vs_number_of_vertices(results, name, log=False, save=False, show=False):
    for max_edges in MAXIMUM_NUMBER_EDGES:
        x = []
        y = []
        for size in range(4, 28):
            x.append(size)
            y.append(results[max_edges][size].time)
        if log:
            plt.semilogy(x, y, label=f"edges ratio: {max_edges}")
        else:
            plt.plot(x, y, label=f"edges ratio: {max_edges}")
        plt.xlabel("Number of vertices")
        plt.ylabel("Time (s)")
        plt.title(f"Time taken vs number of vertices for {name} algorithm")
        plt.legend()

    if save:
        plt.savefig(f"../charts/{name}_time_vs_number_of_vertices.png")
    if show:
        plt.show()
    plt.close()


def plot_number_of_solutions_tested_vs_graph_size(results, name, log=False, save=False, show=False):
    for max_edges in MAXIMUM_NUMBER_EDGES:
        x = []
        y = []
        for size in range(4, 28):
            x.append(size)
            y.append(results[max_edges][size].solution_counter)
        if log:
            plt.semilogy(x, y, label=f"edges ratio: {max_edges}")
        else:
            plt.plot(x, y, label=f"edges ratio: {max_edges}")
        plt.xlabel("Number of vertices")
        plt.ylabel("Number of solutions tested")
        plt.title(f"Number of solutions tested vs number of vertices for {name} algorithm")
        plt.legend()

    if save:
        plt.savefig(f"../charts/{name}_number_of_solutions_tested_vs_graph_size.png")
    if show:
        plt.show()
    plt.close()



def main():
    bruteforce_data = import_data("../results/results_complete_bruteforce_full.pickle")
    greedy_data = import_data("../results/results_complete_greedy_full.pickle")
    plot_number_operations_vs_number_of_vertices(bruteforce_data, "bruteforce", log=True, save=True)
    plot_time_vs_number_of_vertices(bruteforce_data, "bruteforce", log=True, save=True)
    plot_number_of_solutions_tested_vs_graph_size(bruteforce_data, "bruteforce", log=True, save=True)

    plot_number_operations_vs_number_of_vertices(greedy_data, "greedy", log=False, show=True)
    plot_time_vs_number_of_vertices(greedy_data, "greedy", log=False, show=True)
    plot_number_of_solutions_tested_vs_graph_size(greedy_data, "greedy", log=False, show=True)


if __name__ == "__main__":
    main()
