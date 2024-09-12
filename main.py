import json

from validate_xml import validate_xml
from populate_database import populate_database, get_graph_by_id
from parse_json import parse_json
from get_paths import find_all_paths, find_cheapest_path
from create_output_json import create_path_block, create_cheapest_block

ANSWER_JSON = {"answers": []}

if __name__ == "__main__":
    graph, edges = validate_xml("graph_xml.txt")
    populate_database(edges)

    paths, cheapest_paths = parse_json("input.json")
    graph_dd, edges_cost = get_graph_by_id("g0")

    for path in paths:
        all_paths = find_all_paths(graph_dd, path[0], path[1])
        ANSWER_JSON["answers"].append(create_path_block(path[0], path[1], all_paths))

    for cheapest_path in cheapest_paths:
        cheapest = find_cheapest_path(graph_dd, edges_cost, cheapest_path[0], cheapest_path[1])
        ANSWER_JSON["answers"].append(create_cheapest_block(cheapest_path[0], cheapest_path[1], cheapest))

    print(ANSWER_JSON)
