import argparse
import json
from collections import defaultdict

import graph_utils
from models import Edge, Graph
from database import SessionLocal


def populate_database(db, graph, edges):

    graph_model = Graph(**graph)
    db.add(graph_model)
    db.commit()

    for edge in edges:
        edge_model = Edge(**edge)
        db.add(edge_model)
        db.commit()


def get_graph_by_id(db, graph_id):

    graph = defaultdict(list)
    edges_cost = {}
    edges = db.query(Edge).filter(Edge.graph_id == graph_id).all()
    for edge in edges:
        edges_cost[(edge.edge_from, edge.edge_to)] = edge.cost
        if edge.edge_from not in graph:
            graph[edge.edge_from] = [edge.edge_to]
        else:
            graph[edge.edge_from].append(edge.edge_to)
    return graph, edges_cost


def parse_json(input_file):
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
    path_block = {"paths": {"from": start, "to": end, "paths": all_paths}}
    return path_block


def create_cheapest_block(start, end, cheapest_path):
    if not cheapest_path:
        cheapest_path = False
    cheapest_block = {"cheapest": {"from": start, "to": end, "path": cheapest_path}}
    return cheapest_block


def load(db, args):
    graph, edges = graph_utils.loads(args.input)
    populate_database(db, graph, edges)


def query(db, args):
    paths, cheapest_paths = parse_json(args.input)
    graph_dd, edges_cost = get_graph_by_id(db, args.graph_id)

    answer = {"answers": []}

    for path in paths:
        all_paths = graph_utils.find_all_paths(graph_dd, path[0], path[1])
        answer["answers"].append(create_path_block(path[0], path[1], all_paths))

    for cheapest_path in cheapest_paths:
        cheapest = graph_utils.find_cheapest_path(
            graph_dd, edges_cost, cheapest_path[0], cheapest_path[1]
        )
        answer["answers"].append(
            create_cheapest_block(cheapest_path[0], cheapest_path[1], cheapest)
        )

    print(json.dumps(answer))


def main():
    parser = argparse.ArgumentParser()
    sub_cmds = parser.add_subparsers(required=True)

    load_cmd = sub_cmds.add_parser('load')
    load_cmd.set_defaults(func=load)
    load_cmd.add_argument('input')

    query_cmd = sub_cmds.add_parser('query')
    query_cmd.set_defaults(func=query)
    query_cmd.add_argument('graph_id')
    query_cmd.add_argument('input')

    args = parser.parse_args()
    with SessionLocal() as db:
        args.func(db, args)


if __name__ == "__main__":
    main()
