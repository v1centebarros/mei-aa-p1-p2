from itertools import combinations
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