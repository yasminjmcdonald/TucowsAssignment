import argparse
import json
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import interview_test.graph_utils as graph_utils
from interview_test.database_utils import get_graph_by_id, populate_database
from interview_test.json_utils import parse_json, create_path_block, create_cheapest_block
from interview_test.models import Edge, Node, Graph


SQLALCHEMY_DATABASE_URL = os.environ.get(
    'SQLALCHEMY_DATABASE_URL',
    "postgresql://postgres:test1234@localhost/GraphApplicationDatabase"
)


def load(db, args):

    graph, nodes, edges = graph_utils.validate_xml(args.input)
    try:
        populate_database(db, graph, nodes, edges)
    except IntegrityError as e:
        sys.exit(e.orig)


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

    with open(args.output, "w") as handle:
        json.dump(answer, handle)


def main():
    parser = argparse.ArgumentParser()
    sub_cmds = parser.add_subparsers(required=True)

    load_cmd = sub_cmds.add_parser('load', help='Loads graph data from XML into the database')
    load_cmd.set_defaults(func=load)
    load_cmd.add_argument('input', help='graph XML input file')

    query_cmd = sub_cmds.add_parser('query', help='Queries the given graph with '
                                                  'the paths provided in the input file')
    query_cmd.set_defaults(func=query)
    query_cmd.add_argument('graph_id', help='Id of graph')
    query_cmd.add_argument('input', help='JSON input file with queries')
    query_cmd.add_argument('output', help='Name of JSON output file')

    args = parser.parse_args()

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with Session(engine) as db:
        args.func(db, args)


if __name__ == "__main__":
    main()
