import json


def parse_json(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)
    paths = []
    cheapest_paths = []
    for query in data['queries']:
        if "paths" in query:
            paths.append([query['paths']['start'], query['paths']['end']])
        if "cheapest" in query:
            cheapest_paths.append([query['cheapest']['start'], query['cheapest']['end']])
    return paths, cheapest_paths
