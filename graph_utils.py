from collections import defaultdict
import xml.etree.ElementTree as ET


class XmlValidationError(ValueError):
    pass


def loads(contents):
    tree = ET.parse(contents)
    root = tree.getroot()

    if root.find("id") is None:
        raise XmlValidationError(f"id tag but not present in {contents}")
    if root.find("name") is None:
        raise XmlValidationError(f"name tag but not present in {contents}")
    graph = {"id": root.find("id").text, "graph_name": root.find("name").text}
    graph_id = graph.get("id")
    node_ids = set()
    for node in root.find("nodes"):
        node_id = node.find("id").text
        if node_id in node_ids:
            raise XmlValidationError("node ids are not unique")
        node_ids.add(node_id)

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
                "edge_id": edge.find("id").text,
                "graph_id": graph_id,
            }
        )
    return graph, edges


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
