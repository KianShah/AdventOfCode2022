import functools
from collections import defaultdict
from typing import List, Tuple, Dict
from itertools import product
from copy import deepcopy

with open('Day19.txt') as f:
    out = f.read().split('\n')


class Blueprint:
    def __init__(self, ore_bot: int, clay_bot: int, obsidian_bot: Tuple[int, int], geode_bot: Tuple[int, int]):
        self.ore_bot_cost = ore_bot
        self.clay_bot_cost = clay_bot
        self.obsidian_bot_cost = obsidian_bot
        self.geode_bot_cost = geode_bot

    def max_ore_used(self):
        return max(self.ore_bot_cost, self.clay_bot_cost, self.obsidian_bot_cost[0], self.geode_bot_cost[0])

    def max_clay_used(self):
        return self.obsidian_bot_cost[1]

    def max_obsidian_used(self):
        return self.geode_bot_cost[1]


blueprints: List[Blueprint] = []

total_quality = 0

for line in out:
    tokens = line.split(' ')
    ore_bot_cost = int(tokens[6])
    clay_bot_cost = int(tokens[12])
    obsidian_bot_cost = int(tokens[18]), int(tokens[21])
    geode_bot_cost = int(tokens[27]), int(tokens[30])
    blueprints.append(Blueprint(ore_bot_cost, clay_bot_cost, obsidian_bot_cost, geode_bot_cost))

times = defaultdict(int)


def get_max_geodes(blueprint: Blueprint) -> int:
    @functools.lru_cache(maxsize=1024)
    def helper(time: int, robots: Tuple[int, int, int, int], materials: Tuple[int, int, int]) -> int:
        if time == 0:
            return 0

        ores, clay, obsidian = materials

        new_materials = [materials[i] + bot for i, bot in enumerate(robots[:-1])]
        new_robots = [r for r in robots]

        max_geodes_found = 0
        if ores < (blueprint.max_ore_used()-robots[0])*time and clay < (blueprint.max_clay_used()-robots[1])*time and obsidian < (blueprint.max_obsidian_used()-robots[2])*time:
            max_geodes_found = max(max_geodes_found, helper(time - 1, tuple(new_robots), tuple(new_materials)))

        ore_needed, obsidian_needed = blueprint.geode_bot_cost
        if ores >= ore_needed and obsidian >= obsidian_needed:
            new_materials[0] -= ore_needed
            new_materials[2] -= obsidian_needed
            new_robots[3] += 1
            max_geodes_found = max(max_geodes_found, helper(time - 1, tuple(new_robots), tuple(new_materials)))
        else:
            ore_needed = blueprint.ore_bot_cost
            if ores >= ore_needed and robots[0] < blueprint.max_ore_used():
                new_materials[0] -= ore_needed
                new_robots[0] += 1
                max_geodes_found = max(max_geodes_found, helper(time - 1, tuple(new_robots), tuple(new_materials)))
                new_robots[0] -= 1
                new_materials[0] += ore_needed

            ore_needed = blueprint.clay_bot_cost
            if ores >= ore_needed and robots[1] < blueprint.max_clay_used():
                new_materials[0] -= ore_needed
                new_robots[1] += 1
                max_geodes_found = max(max_geodes_found, helper(time - 1, tuple(new_robots), tuple(new_materials)))
                new_robots[1] -= 1
                new_materials[0] += ore_needed

            ore_needed, clay_needed = blueprint.obsidian_bot_cost
            if ores >= ore_needed and clay >= clay_needed and robots[2] < blueprint.max_obsidian_used():
                new_materials[0] -= ore_needed
                new_materials[1] -= clay_needed
                new_robots[2] += 1
                max_geodes_found = max(max_geodes_found, helper(time - 1, tuple(new_robots), tuple(new_materials)))

        return robots[-1] + max_geodes_found

    return helper(24, (1, 0, 0, 0), (0, 0, 0))


for i, b in enumerate(blueprints):
    max_geodes = get_max_geodes(b)
    print(f"Finished blueprint {i+1}")
    total_quality += max_geodes * (i + 1)

print(total_quality)
