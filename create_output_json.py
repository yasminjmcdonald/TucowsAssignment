def create_path_block(start, end, all_paths):
    path_block = {"paths": {"from": start, "to": end, "paths": all_paths}}
    return path_block


def create_cheapest_block(start, end, cheapest_path):
    if not cheapest_path:
        cheapest_path = False
    cheapest_block = {"cheapest": {"from": start, "to": end, "path": cheapest_path}}
    return cheapest_block
