from collections import defaultdict

from interview_test.models import Edge, Node, Graph


def populate_database(db, graph, nodes, edges):
    """
    Populates database tables graphs, nodes and edges with
    the graph, nodes, and edges parameters.
    Args:
        :param db: Database session object.
        :param graph: Dictionary with graph properties.
        :param nodes: List of dictionaries with node properties.
        :param edges: List of dictionaries with edge properties.
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
        :param graph_id: ID of graph.
    Returns:
        graph: Dictionary of directed graph.
        edges_cost: Dictionary with graph edges and corresponding costs.
    """
    graph = defaultdict(list)
    edges_cost = {}
    edges = db.query(Edge).filter(Edge.graph == graph_id).all()
    for edge in edges:
        edges_cost[(edge.edge_from, edge.edge_to)] = edge.cost
        if edge.edge_from not in graph:
            graph[edge.edge_from] = [edge.edge_to]
        else:
            graph[edge.edge_from].append(edge.edge_to)
    return graph, edges_cost
