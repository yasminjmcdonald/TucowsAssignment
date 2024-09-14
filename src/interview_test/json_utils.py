import json

import interview_test.graph_utils as graph_utils


def parse_query_json(input_file):
    """
    Reads and parses JSON file of queries. Returns paths
    and cheapest_paths to be queried.
    Args:
        :param input_file: JSON file with queries.
    Returns:
        paths: List of paths to query.
        cheapest_paths: List of cheapest paths to query.
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
    Ex: {"paths": {"from": "a", "to": "b", "paths": [["a", "b"]]}}
    Args:
        :param start: Start node of path.
        :param end: End node of path.
        :param all_paths: List of paths.
    Returns:
        paths_block: JSON object with start node,
        end node, and all paths.
    """
    return {"paths": {"from": start, "to": end, "paths": all_paths}}


def create_cheapest_block(start, end, cheapest_path):
    """
    Creates path block for JSON output file.
    Ex: {"cheapest": {"from": "a", "to": "b", "path": [["a", "b"]]}}
    Args:
        :param start: Start node of path.
        :param end: End node of path.
        :param cheapest_path: Cheapest path between start.
        node and end node.
    Returns:
        paths_block: JSON object with start node,
        end node, and cheapest path.
    """
    if not cheapest_path:
        cheapest_path = False
    return {"cheapest": {"from": start, "to": end, "path": cheapest_path}}


def create_answer_json(graph_dd, edge_cost, paths, cheapest_paths):
    """
    Find all paths in from start to end node pairs in paths Lists.
    Finds cheapest paths between start and end node pairs in cheapest_paths
    Lists. Returns answer JSON.
    Args:
        :param graph_dd: Dictionary of directed graph.
        :param edge_cost: Dictionary of edges and corresponding costs.
        :param paths: List of paths to be queried.
        node and end node.
        :param cheapest_paths: List of cheapest paths to be queried.
    Returns:
        answers: JSON object with answers
    """
    answers = {"answers": []}

    for path in paths:
        all_paths = graph_utils.find_all_paths(graph_dd, path[0], path[1])
        answers["answers"].append(create_path_block(path[0], path[1], all_paths))

    for cheapest_path in cheapest_paths:
        cheapest = graph_utils.find_cheapest_path(
            graph_dd, edge_cost, cheapest_path[0], cheapest_path[1]
        )
        answers["answers"].append(
            create_cheapest_block(cheapest_path[0], cheapest_path[1], cheapest)
        )
    return answers

