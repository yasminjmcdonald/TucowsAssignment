import json


def parse_json(input_file):
    """
    Reads and parses JSON file of queries. Returns paths
    and cheapest_paths queries.
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
    Create path block for JSON output file.
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
    Create path block for JSON output file.
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

