import sys
from collections import defaultdict

from interview_test.models import Edge, Node, Graph


def populate_database(db, graph, nodes, edges):
    """
    Populates database tables graphs, nodes and edges with
    the graph, nodes, and edges parameters.
    Args:
        :param db: Database session object.
        :param graph: Dictionary with graph properties.
        Ex. {"id": "g0", "name": "Graph Name"}
        :param nodes: List of dictionaries with node properties.
        Ex. [{"id": "a", "graph": "g0", "name": "Graph Name"}]
        :param edges: List of dictionaries with edge properties.
        Ex. [{"edge_to": "a", "edge_from": "b", "cost": 0.0, "id": "e1", "graph": "g0"}]
    Returns:
    """
    graph_model = Graph(**graph)
    db.add(graph_model)
    db.commit()
    for node in nodes:
        node_model = Node(**node)
        db.add(node_model)
        db.commit()
    for edge in edges:
        edge_model = Edge(**edge)
        db.add(edge_model)
        db.commit()


def get_graph_by_id(db, graph_id):
    """
    Queries graphs table by graph_id and returns two
    dictionaries.
    Args:
        :param db: Database session object.
        :param graph_id: ID of graph. Ex. "g0"
    Returns:
        graph: Dictionary of directed graph.
        Ex. {"a": ["b", "c"], "b": ["e"], "c": ["e"]}
        edges_cost: Dictionary with graph edges and corresponding costs.
        Ex. {("a", "b"): 0.0, ("a", "c"): 0.42}
    """
    graph = defaultdict(list)
    edges_cost = {}
    edges = db.query(Edge).filter(Edge.graph == graph_id).all()
    if not edges:
        sys.exit(f"Graph {graph_id} does not exist")
    for edge in edges:
        edges_cost[(edge.edge_from, edge.edge_to)] = edge.cost
        if edge.edge_from not in graph:
            graph[edge.edge_from] = [edge.edge_to]
        else:
            graph[edge.edge_from].append(edge.edge_to)
    return graph, edges_cost
