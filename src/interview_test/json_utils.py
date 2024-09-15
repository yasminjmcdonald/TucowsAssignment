import json

import interview_test.graph_utils as graph_utils


def parse_query_json(input_file):
    """
    Reads and parses JSON file of queries. Returns paths
    and cheapest_paths to be queried.
    Args:
        :param input_file: JSON file with queries.
    Returns:
        paths: List of paths to query. Ex. [["a", "d"], ["a", "e"]]
        cheapest_paths: List of cheapest paths to query.
        Ex. [["a", "d"], ["a", "e"]]
    """
    with open(input_file, "r") as file:
        data = json.load(file)
    paths = []
    cheapest_paths = []
    for query in data["queries"]:
        if "paths" in query:
            paths.append([query["paths"]["start"], query["paths"]["end"]])
        if "cheapest" in query:
            cheapest_paths.append(
                [query["cheapest"]["start"], query["cheapest"]["end"]]
            )
    return paths, cheapest_paths


def create_path_block(start, end, all_paths):
    """
    Creates path block for JSON output file.
    Args:
        :param start: Start node of path. Ex. "a"
        :param end: End node of path. Ex. "e"
        :param all_paths: List of paths. [["a", "b", "e"], ["a", "d", "e"]]
    Returns:
        paths_block: JSON object with start node,
        end node, and all paths.
        Ex: {"paths": {"from": "a", "to": "e", "paths": [["a", "b", "e"], ["a", "d", "e"]]}}
    """
    return {"paths": {"from": start, "to": end, "paths": all_paths}}


def create_cheapest_block(start, end, cheapest_path):
    """
    Creates path block for JSON output file.
    Args:
        :param start: Start node of path. Ex. "a"
        :param end: End node of path. Ex. "e"
        :param cheapest_path: Cheapest path to be queried. Ex. ["a", "e"]
    Returns:
        paths_block: JSON object with start node,
        end node, and cheapest path.
         Ex: {"cheapest": {"from": "a", "to": "e", "path": [["a", "e"]]}}
    """
    if not cheapest_path:
        cheapest_path = False
    return {"cheapest": {"from": start, "to": end, "path": cheapest_path}}


def create_answer_json(graph_dd, edges_cost, paths, cheapest_paths):
    """
    Find all paths in from start to end node pairs in paths Lists.
    Finds cheapest paths between start and end node pairs in cheapest_paths
    Lists. Returns answer JSON.
    Args:
        :param graph_dd: Dictionary of directed graph.
         Ex. {"a": ["b", "c"], "b": ["e"], "c": ["e"]}
        :param edges_cost: Dictionary of edges and corresponding costs.
        Ex. {("a", "b"): 0.0, ("a", "c"): 0.42}
        :param paths: List of paths to be queried. Ex. [["a", "e"], ["a", "d"]]
        node and end node.
        :param cheapest_paths: List of cheapest paths to be queried.
        Ex. [["a", "d"], ["a", "e"]]
    Returns:
        answers: JSON object with answers
    """
    answers = {"answers": []}

    for path in paths:
        all_paths = graph_utils.find_all_paths(graph_dd, path[0], path[1])
        answers["answers"].append(create_path_block(path[0], path[1], all_paths))

    for cheapest_path in cheapest_paths:
        cheapest = graph_utils.find_cheapest_path(
            graph_dd, edges_cost, cheapest_path[0], cheapest_path[1]
        )
        answers["answers"].append(
            create_cheapest_block(cheapest_path[0], cheapest_path[1], cheapest)
        )
    return answers
