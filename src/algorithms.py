from itertools import combinations
from utils import benchmark

"""
    This function is slower than the one below
"""


# def is_vertex_cover(graph, vertices):
#     return all([u in vertices or v in vertices for u, v in graph.edges()])

def is_vertex_cover(graph, vertices):
    operation_count = 0  # Initialize operation counter
    for u, v in graph.edges():
        operation_count += 1
        if u not in vertices and v not in vertices:
            operation_count += 1
            return False, operation_count  # Return operation count
    return True, operation_count  # Return operation count


@benchmark
def bruteforce(graph):
    cover = set()
    operation_count = 0  # Initialize operation counter

    # Iterate over all possible subsets of vertices
    for i in range(1, len(graph.nodes()) + 1):
        for vertices in combinations(graph.nodes(), i):
            operation_count += 1  # Increment operation counter for each combination
            is_cover, oc = is_vertex_cover(graph, vertices)
            operation_count += oc
            if is_cover:
                operation_count += 1  # Increment operation counter for each check
                if len(cover) == 0 or len(vertices) < len(cover):
                    cover = set(vertices)

    return cover, operation_count  # Return operation count


@benchmark
def bruteforce_bitwise(graph):
    """
        :deprecated: This function is deprecated because it is slower than bruteforce
    """
    cover = set()
    operation_count = 0  # Initialize operation counter

    # Iterate over all possible subsets of vertices
    for i in range(1, 2 ** len(graph.nodes())):
        vertices = set()
        for j in range(len(graph.nodes())):
            operation_count += 1  # Increment operation counter for each bitwise operation
            if i & (1 << j):
                vertices.add(j)
        if is_vertex_cover(graph, vertices):
            operation_count += 1  # Increment operation counter for each check
            if len(cover) == 0 or len(vertices) < len(cover):
                cover = set(vertices)

    return cover, operation_count  # Return operation count


@benchmark
def greedy_vertex_cover(graph):
    cover = set()
    operation_count = 0  # Initialize operation counter

    # As long as there are edges in the graph
    while graph.number_of_edges() > 0:
        operation_count += 1  # Increment operation counter for each edge check
        # Select the vertex with the highest degree
        v = max(graph.degree, key=lambda x: x[1])[0]
        operation_count += 1  # Increment operation counter for each vertex selection

        # Add the vertex to the cover and remove it from the graph
        cover.add(v)
        graph.remove_node(v)
        operation_count += 2  # Increment operation counter for each addition and removal

    return cover, operation_count  # Return operation count
