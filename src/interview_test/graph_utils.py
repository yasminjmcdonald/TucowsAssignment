from collections import defaultdict
import xml.etree.ElementTree as ET


class XmlValidationError(ValueError):
    pass


def validate_xml(contents):
    """
    Validates contents of a graph XML file and returns
    graph, nodes, and edges.
    Args:
        :param contents: XML file with directed graph.
    Returns:
        graph: Ex. {"id": "g0", "name": "Graph Name"}
        nodes: Ex. [{"id": "a", "graph": "g0", "name": "Graph Name"}]
        edges: Ex. [{"edge_to": "a", "edge_from": "b",
        "cost": 0.0, "id": "e1", "graph": "g0"}]
    """
    tree = ET.parse(contents)
    root = tree.getroot()

    if root.find("id") is None:
        raise XmlValidationError(f"id tag not present in {contents}")
    if root.find("name") is None:
        raise XmlValidationError(f"name tag not present in {contents}")

    graph = {"id": root.find("id").text, "name": root.find("name").text}
    graph_id = graph.get("id")

    nodes = []
    node_ids = set()
    for node in root.find("nodes"):
        node_id = node.find("id").text
        if node_id in node_ids:
            raise XmlValidationError("node ids are not unique")
        node_ids.add(node_id)
        nodes.append({"id": node_id, "graph": graph_id, "name": node.find("name").text})

    if not node_ids:
        raise XmlValidationError("expected 1 or more nodes")

    edges = []

    for edge in root.find("edges"):
        if len(edge.findall("from")) > 1:
            raise XmlValidationError("cannot have more than one 'from' tag in an edge")
        if len(edge.findall("to")) > 1:
            raise XmlValidationError("cannot have more than one 'to' tag in an edge")
        from_tag = edge.find("from").text
        to_tag = edge.find("to").text
        if from_tag not in node_ids:
            raise XmlValidationError(f"{from_tag} node id does not exist")
        if to_tag not in node_ids:
            raise XmlValidationError(f"{to_tag} node id does not exist")
        if (cost_tag := edge.find("cost")) is not None:
            cost = float(cost_tag.text)
        else:
            cost = 0.0
        edges.append(
            {
                "edge_to": to_tag,
                "edge_from": from_tag,
                "cost": cost,
                "id": edge.find("id").text,
                "graph": graph_id,
            }
        )
    return graph, nodes, edges


def find_all_paths(graph: defaultdict, start, end, path=None):
    """
    Finds all paths between start and end nodes.
    Args:
        :param graph: Dictionary of directed graph.
        Ex. {"a": ["b", "c"], "b": ["e"], "c": ["e"]}
        :param start: Start node. Ex. "a"
        :param end: End nodes. Ex. "e"
        :param path: Default None.
    Returns:
        paths: List of paths. Ex. [["a", "b", "e"], ["a", "c", "e"]]
    """
    if path is None:
        path = []
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


def find_cheapest_path(graph: defaultdict, edges_cost, start, end, path=None):
    """
    Finds the cheapest path between start and end nodes.
    Args:
        :param graph: Dictionary of directed graph.
        Ex. {"a": ["b", "c"], "b": ["e"], "c": ["e"]}
        :param start: Start node. Ex. "a"
        :param end: End nodes. Ex. "e"
        :param edges_cost: Dictionary of edges and
        corresponding costs. Ex. {("a", "b"): 0.0, ("a", "c"): 0.42}
        :param path: Default None.
    Returns:
        shortest: The cheapest path between the start and end node.
        Ex. ["a", "b", "e"]
    """
    if path is None:
        path = []
    path = path + [start]
    if start == end:
        return path
    shortest = None
    weight = None
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
