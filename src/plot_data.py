import os
from pprint import pprint

from matplotlib import pyplot as plt
from utils import MAXIMUM_NUMBER_EDGES,NUMBER_OF_ITERATIONS, import_data


def plot_number_operations_vs_number_of_vertices(results, name, log=False, save=False, show=False):
    for max_edges in MAXIMUM_NUMBER_EDGES:
        x = []
        y = []
        for size in range(4, 256):
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
        for size in range(4, 256):
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
        for size in range(4, 256):
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


def plot_full_results(results, name, log=False, save=False, show=False):
    plot_number_operations_vs_number_of_vertices(results, name, log=log, show=show, save=save)
    plot_time_vs_number_of_vertices(results, name, log=log, show=show, save=save)
    plot_number_of_solutions_tested_vs_graph_size(results, name, log=log, show=show, save=save)


def main():
    # Open all the files that start with results_adaptive_randomized_vertex_cover
    files = [f for f in os.listdir("../results") if f.startswith("results_adaptive_randomized_vertex_cover")]
    # Load all the files
    results = [import_data(f"../results/{file}") for file in files]
    # Plot all the files
    for i, result in zip(NUMBER_OF_ITERATIONS,results):
        plot_full_results(result, f"adaptive_randomized_{i}", log=True, save=True)

    files = [f for f in os.listdir("../results") if f.startswith("results_random_vertex_cover")]

    results = [import_data(f"../results/{file}") for file in files]
    for i, result in zip(NUMBER_OF_ITERATIONS, results):
        plot_full_results(result, f"random_{i}", log=True, save=True)


if __name__ == "__main__":
    main()
