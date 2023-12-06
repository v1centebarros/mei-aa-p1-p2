import random
from itertools import combinations
from math import ceil

from utils import benchmark, deprecated


def is_vertex_cover(graph, vertices):
    operation_count = 0  # Initialize operation counter
    for u, v in graph.edges():
        operation_count += 1
        if u not in vertices and v not in vertices:
            operation_count += 1
            return False, operation_count  # Return early if not a vertex cover
    return True, operation_count  # All edges are covered


@benchmark
def bruteforce(graph):
    cover = set()
    operation_count = 0  # Initialize operation counter
    solution_counter = 0  # Initialize solution counter

    for i in range(1, len(graph.nodes()) + 1):
        for vertices in combinations(graph.nodes(), i):
            operation_count += 1  # Increment operation counter for each combination
            is_cover, oc = is_vertex_cover(graph, vertices)
            operation_count += oc
            if is_cover:
                solution_counter += 1  # Increment solution counter for each valid cover
                operation_count += 1  # Increment operation counter for each check
                if not cover or len(vertices) < len(cover):
                    operation_count += 1
                    cover = set(vertices)

    return cover, operation_count, solution_counter  # Return all counts


@benchmark
def greedy_vertex_cover(graph):
    # This variable will count the number of operations
    operations_count = 0

    # This variable will count the number of solutions tested (which in greedy approach is typically the number of iterations)
    solutions_tested = 0

    # The set to store the vertices in the vertex cover
    vertex_cover = set()

    # While there are edges in the graph
    while graph.number_of_edges() > 0:
        # Increase the solutions tested count
        solutions_tested += 1

        # Find the vertex with the maximum degree
        max_degree_node = max(graph.degree, key=lambda x: x[1])[0]
        operations_count += graph.degree[max_degree_node]  # Increment operation count by the degree of the chosen node

        # Add it to the vertex cover
        vertex_cover.add(max_degree_node)

        # Remove the vertex and all its edges from the graph
        graph.remove_node(max_degree_node)

    return vertex_cover, operations_count, solutions_tested


@benchmark
def randomized_vertex_cover(graph, iterations=1000):
    best_cover = None
    operations_count = 0
    solution_counter = 0
    total_vertices = len(graph.nodes())
    checked_subsets = set()  # To track already checked subsets

    for i in range(iterations):
        subset_size = max(1, ceil(total_vertices * (1 - i / iterations)))
        random_subset = random.sample(graph.nodes(), subset_size)
        operations_count += 1

        subset_key = frozenset(random_subset)  # Immutable set as a key
        if subset_key not in checked_subsets:
            solution_counter += 1
            operations_count += 1
            checked_subsets.add(subset_key)
            is_cover, additional_ops = is_vertex_cover(graph, random_subset)
            operations_count += additional_ops

            if is_cover and (not best_cover or len(random_subset) < len(best_cover)):
                operations_count += 1
                best_cover = set(random_subset)

    return best_cover, operations_count, solution_counter


@benchmark
def randomized_vertex_cover_min(graph, iterations=1000):
    best_cover = None
    operations_count = 0
    solution_counter = 0
    total_vertices = len(graph.nodes())
    checked_subsets = set()

    for i in range(iterations):
        subset_size = min(total_vertices, ceil((i + 1) / iterations * total_vertices))
        random_subset = random.sample(graph.nodes(), subset_size)
        operations_count += 1

        subset_key = frozenset(random_subset)
        if subset_key not in checked_subsets:
            operations_count += 1
            solution_counter += 1
            checked_subsets.add(subset_key)
            is_cover, additional_ops = is_vertex_cover(graph, random_subset)
            operations_count += additional_ops

            if is_cover and (not best_cover or len(random_subset) < len(best_cover)):
                operations_count += 1
                best_cover = set(random_subset)

    return best_cover, operations_count, solution_counter


@benchmark
def adaptive_randomized_vertex_cover(graph, iterations=1000, improvement_threshold=10):
    best_cover = None
    operations_count = 0
    solution_counter = 0
    total_vertices = len(graph.nodes())
    last_improvement = 0
    subset_size = total_vertices
    checked_subsets = set()

    for i in range(iterations):
        random_subset = random.sample(graph.nodes(), subset_size)
        operations_count += 1

        subset_key = frozenset(random_subset)
        if subset_key not in checked_subsets:
            operations_count += 1
            solution_counter += 1
            checked_subsets.add(subset_key)
            is_cover, additional_ops = is_vertex_cover(graph, random_subset)
            operations_count += additional_ops

            if is_cover:
                operations_count += 1
                if not best_cover or len(random_subset) < len(best_cover):
                    operations_count += 1
                    best_cover = set(random_subset)
                    last_improvement = i
                elif i - last_improvement > improvement_threshold:
                    operations_count += 1
                    subset_size = max(1, subset_size - 2)
                    last_improvement = i
            else:
                operations_count += 1
                subset_size = max(1, subset_size - 1)

    return best_cover, operations_count, solution_counter
