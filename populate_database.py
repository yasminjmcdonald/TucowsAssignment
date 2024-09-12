from database import SessionLocal
from get_paths import find_all_paths
from models import Edges
from collections import defaultdict


def populate_database(edges):
    db = SessionLocal()

    for edge in edges:
        edge_model = Edges(**edge)
        db.add(edge_model)
        db.commit()
    db.close()


def get_graph_by_id(graph_id):
    db = SessionLocal()

    graph = defaultdict(list)
    edges_cost = {}
    edges = db.query(Edges).filter(Edges.graph_id == graph_id).all()
    for edge in edges:
        edges_cost[(edge.edge_from, edge.edge_to)] = edge.cost
        if edge.edge_from not in graph:
            graph[edge.edge_from] = [edge.edge_to]
        else:
            graph[edge.edge_from].append(edge.edge_to)
    db.close()
    return graph, edges_cost


