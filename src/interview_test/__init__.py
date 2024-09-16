import argparse
import os
import sys

from json.decoder import JSONDecodeError
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from xml.etree.ElementTree import ParseError

import interview_test.graph_utils as graph_utils
from interview_test.database_utils import get_graph_by_id, populate_database
from interview_test.json_utils import *
from interview_test.models import Edge, Node, Graph


SQLALCHEMY_DATABASE_URL = os.environ.get(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql://postgres:test1234@localhost/GraphApplicationDatabase"
)


def load(db, args):
    """
    Loads graph data from graph XML into database tables.
    Args:
        :param db: Database session object.
        :param args: Command line arguments.
    Returns:
    """
    try:
        graph, nodes, edges = graph_utils.validate_xml(args.input)
        populate_database(db, graph, nodes, edges)
    except IntegrityError as e:
        sys.exit(e.orig)
    except ParseError as e:
        sys.exit(f"Error occurred when parsing {args.input}: {e.msg}")


def query(db, args):
    """
    Queries graph table with queries defined in JSON input file and outputs
    JSON file with answers.
    Args:
        :param db: Database session object.
        :param args: Command line arguments.
    Returns:
    """
    try:
        paths, cheapest_paths = parse_query_json(args.input)
        graph_dd, edges_cost = get_graph_by_id(db, args.graph_id)
        answers = create_answer_json(graph_dd, edges_cost, paths, cheapest_paths)
        with open(args.output, "w") as handle:
            json.dump(answers, handle)
    except JSONDecodeError as e:
        sys.exit(f"Error occurred when parsing {args.input}: {e.args}")


def main():
    parser = argparse.ArgumentParser()
    sub_cmds = parser.add_subparsers(required=True)

    load_cmd = sub_cmds.add_parser(
        "load", help="Loads graph data from XML into the database"
    )
    load_cmd.set_defaults(func=load)
    load_cmd.add_argument("input", help="graph XML input file")

    query_cmd = sub_cmds.add_parser(
        "query",
        help="Queries the given graph with " "the paths provided in the input file",
    )
    query_cmd.set_defaults(func=query)
    query_cmd.add_argument("graph_id", help="Id of graph")
    query_cmd.add_argument("input", help="JSON input file with queries")
    query_cmd.add_argument("output", help="Name of JSON output file")

    args = parser.parse_args()

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with Session(engine) as db:
        args.func(db, args)


if __name__ == "__main__":
    main()
