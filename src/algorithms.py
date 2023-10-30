from itertools import combinations
from utils import time_algorithm


def is_vertex_cover(graph, vertices):
    return all([u in vertices or v in vertices for u, v in graph.edges()])

@time_algorithm
def bruteforce(graph):
    cover = set()

    # Iterate over all possible subsets of vertices
    for i in range(1, len(graph.nodes()) + 1):
        for vertices in combinations(graph.nodes(), i):
            if is_vertex_cover(graph, vertices):
                if len(cover) == 0 or len(vertices) < len(cover):
                    cover = set(vertices)

    return cover

@time_algorithm
def bruteforce_bitwise(graph):
    cover = set()

    # Iterate over all possible subsets of vertices
    for i in range(1, 2**len(graph.nodes())):
        vertices = set()
        for j in range(len(graph.nodes())):
            if i & (1 << j):
                vertices.add(j)
        if is_vertex_cover(graph, vertices):
            if len(cover) == 0 or len(vertices) < len(cover):
                cover = set(vertices)

    return cover


@time_algorithm
def greedy_vertex_cover(graph):
    # Initialize the vertex cover as an empty set
    cover = set()

    # As long as there are edges in the graph
    while graph.number_of_edges() > 0:
        # Select the vertex with the highest degree
        v = max(graph.degree, key=lambda x: x[1])[0]

        # Add the vertex to the cover and remove it from the graph
        cover.add(v)
        graph.remove_node(v)

    return cover