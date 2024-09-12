from collections import defaultdict


def find_all_paths(graph: defaultdict, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node in graph[start]:
        if node not in path:
            new_paths = find_all_paths(graph, node, end, path)
        for new_path in new_paths:
            paths.append(new_path)
    return paths


def find_cheapest_path(graph: defaultdict, edges_cost, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    shortest = None
    weight: float
    for node in graph[start]:
        if node not in path:
            new_path = find_cheapest_path(graph, edges_cost, node, end, path)
            if new_path:
                new_path_weight = 0
                for i in range(len(new_path) - 1):
                    new_path_weight += edges_cost[(new_path[i], new_path[i + 1])]
                if not shortest or new_path_weight < weight:
                    weight = new_path_weight
                    shortest = new_path
    return shortest



