from typing import Tuple, List, Dict, Set
import json

with open('Day16.txt') as f:
    out = f.read().split('\n')

location_mappings: Dict[str, List[str]] = {}
flow_rates: Dict[str, int] = {}

for line in out:
    valve_desc, dests = line.split('; ')
    tokens = valve_desc.split(' ')
    valve = tokens[1]
    rate = int(tokens[4][5:])
    flow_rates[valve] = rate

    locations = dests[23:].split(', ')
    location_mappings[valve] = locations

non_negs = {valve for valve, flow_rate in flow_rates.items() if flow_rate > 0}

location_mappings_with_dists: Dict[str, List[Tuple[str, int]]] = {}


def DFS(curr_node, dest_node: str, curr_depth: int):
    if flow_rates[dest_node] > 0 and curr_depth > 0:
        location_mappings_with_dists[curr_node] = location_mappings_with_dists[curr_node] + [(dest_node, curr_depth)]
        location_mappings_with_dists[dest_node] = location_mappings_with_dists[dest_node] + [(curr_node, curr_depth)]
        DFS(dest_node, dest_node, 0)
    else:
        curr_depth += 1
        for n in location_mappings[curr_node]:
            DFS(curr_node, n, curr_depth)


def traverse(curr_node: str, curr_time: int) -> int:
    if curr_time == 0:
        return 0
    curr_max = 0
    new_time = curr_time - 1
    if flow_rates[curr_node] > 0:
        new_total = flow_rates[curr_node] * new_time
        temp = flow_rates[curr_node]
        flow_rates[curr_node] = 0
        new_total += traverse(curr_node, new_time)
        flow_rates[curr_node] = temp
        curr_max = max(curr_max, new_total)

    for new_node in location_mappings[curr_node]:
        curr_max = max(curr_max, traverse(new_node, new_time))
    return curr_max


DFS('AA', 'AA', 0)
print(location_mappings_with_dists)
