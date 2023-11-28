import random
from itertools import combinations
from math import ceil

from utils import benchmark


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
def randomized_vertex_cover(graph):
    operations_count = 0
    solutions_tested = 0

    vertex_cover = set()

    vertices = list(graph.nodes())
    random.shuffle(vertices)

    for v in vertices:
        solutions_tested += 1

        for u in graph.neighbors(v):
            operations_count += 1
            if (u, v) not in vertex_cover and (v, u) not in vertex_cover:
                vertex_cover.add(v)
                break

    return vertex_cover, operations_count, solutions_tested


@benchmark
def monte_carlo_vertex_cover(graph, iterations=1000):
    best_cover = set(graph.nodes())
    operations_count = 0

    for _ in range(iterations):
        random_cover = set(random.sample(graph.nodes(), k=random.randint(1, len(graph.nodes()))))
        operations_count += 1  # For the sampling operation

        if is_vertex_cover(graph, random_cover)[0] and len(random_cover) < len(best_cover):
            best_cover = random_cover

    return best_cover, operations_count, iterations


@benchmark
def improved_randomized_vertex_cover_fixed_sample_length(graph, iterations=10000):
    best_cover = None
    operations_count = 0
    solution_counter = 0

    for _ in range(iterations):
        subset_size = random.randint(1, len(graph.nodes()))
        random_subset = random.sample(graph.nodes(), subset_size)
        operations_count += 1

        is_cover, additional_ops = is_vertex_cover(graph, random_subset)
        operations_count += additional_ops

        if is_cover:
            solution_counter += 1
            if best_cover is None or len(random_subset) < len(best_cover):
                best_cover = set(random_subset)

    return best_cover, operations_count, solution_counter

@benchmark
def improved_randomized_vertex_cover(graph, iterations=1000):
    best_cover = None
    operations_count = 0
    solution_counter = 0
    total_vertices = len(graph.nodes())

    # Start with a larger subset and decrease the size over iterations
    for i in range(iterations):
        # Gradually decrease the subset size, ensuring it's always at least 1
        subset_size = max(1, ceil(total_vertices * (1 - i / iterations)))
        random_subset = random.sample(graph.nodes(), subset_size)
        operations_count += 1

        is_cover, additional_ops = is_vertex_cover(graph, random_subset)
        operations_count += additional_ops

        if is_cover:
            solution_counter += 1
            if best_cover is None or len(random_subset) < len(best_cover):
                best_cover = set(random_subset)

    return best_cover, operations_count, solution_counter


@benchmark
def adaptive_randomized_vertex_cover(graph, iterations=1000):
    best_cover = None
    operations_count = 0
    solution_counter = 0
    total_vertices = len(graph.nodes())

    # Parameters for adaptive sizing
    last_improvement = 0
    improvement_threshold = 10  # Number of iterations without improvement to adjust subset size
    subset_size = total_vertices

    for i in range(iterations):
        random_subset = random.sample(graph.nodes(), subset_size)
        operations_count += 1

        is_cover, additional_ops = is_vertex_cover(graph, random_subset)
        operations_count += additional_ops

        if is_cover:
            solution_counter += 1
            if best_cover is None or len(random_subset) < len(best_cover):
                best_cover = set(random_subset)
                last_improvement = i  # Update the last improvement iteration
            else:
                if i - last_improvement > improvement_threshold:
                    # Decrease the subset size more aggressively if no recent improvements
                    subset_size = max(1, subset_size - 2)
                    last_improvement = i  # Reset improvement counter
        else:
            # Slightly decrease subset size over time
            subset_size = max(1, subset_size - 1)

    return best_cover, operations_count, solution_counter


@benchmark
def adaptative_with_local_search_random_vertex_cover(graph, iterations=1000, local_search_iterations=250):
    best_cover = None
    operations_count = 0
    solution_counter = 0
    total_vertices = len(graph.nodes())

    # Adaptive sizing parameters
    last_improvement = 0
    improvement_threshold = 10
    subset_size = total_vertices

    for i in range(iterations):
        random_subset = random.sample(graph.nodes(), subset_size)
        operations_count += 1

        is_cover, additional_ops = is_vertex_cover(graph, random_subset)
        operations_count += additional_ops

        if is_cover:
            solution_counter += 1
            if best_cover is None or len(random_subset) < len(best_cover):
                best_cover = set(random_subset)
                last_improvement = i

                # Local Search Optimization
                for _ in range(local_search_iterations):
                    if len(best_cover) <= 1:
                        break
                    vertex_to_remove = random.choice(list(best_cover))
                    new_cover = best_cover - {vertex_to_remove}
                    operations_count += 1

                    if is_vertex_cover(graph, new_cover)[0]:
                        best_cover = new_cover  # Found a smaller valid cover
                    else:
                        operations_count += 1  # For the failed cover check
            else:
                if i - last_improvement > improvement_threshold:
                    subset_size = max(1, subset_size - 2)
                    last_improvement = i
        else:
            subset_size = max(1, subset_size - 1)

    return best_cover, operations_count, solution_counter
