from collections import deque
from time import perf_counter
from typing import Tuple, List

with open('Day18.txt') as f:
    out = f.read().split('\n')

cubes = set()

for cube in out:
    x, y, z = [int(a) for a in cube.split(',')]
    cubes.add((x, y, z))

# Part 1
# def surface_area(lst: List[Tuple[int, int, int]]) -> int:
#     res = 0
#     for x, y, z in lst:
#         res += 6
#         if (x - 1, y, z) in cubes:
#             res -= 1
#         if (x + 1, y, z) in cubes:
#             res -= 1
#         if (x, y - 1, z) in cubes:
#             res -= 1
#         if (x, y + 1, z) in cubes:
#             res -= 1
#         if (x, y, z - 1) in cubes:
#             res -= 1
#         if (x, y, z + 1) in cubes:
#             res -= 1
#
#     return res

# print(surface_area(cubes))

# Part 2
is_air_pocket_memo = set()
is_not_air_pocket_memo = set()


def get_neighbours(coords: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    x, y, z = coords
    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1)
    ]


def has_escaped(coords: Tuple[int, int, int]) -> bool:
    for c in coords:
        if not 1 <= c <= 20:
            return True
    return False


# BFS
def is_air_pocket(coords: Tuple[int, int, int]) -> bool:
    if coords in is_air_pocket_memo:
        return True
    visited = {coords}
    queue = deque([coords])
    while len(queue) > 0:
        toVisit = queue.popleft()
        if toVisit in is_not_air_pocket_memo or has_escaped(toVisit):
            for v in visited:
                is_not_air_pocket_memo.add(v)
            return False
        for n in get_neighbours(toVisit):
            if n not in visited and n not in cubes:
                visited.add(n)
                queue.append(n)
    for v in visited:
        is_air_pocket_memo.add(v)
    return True


def surface_area(lst: List[Tuple[int, int, int]]) -> int:
    res = 0
    for x, y, z in lst:
        if (x - 1, y, z) not in cubes and not is_air_pocket((x - 1, y, z)):
            res += 1
        if (x + 1, y, z) not in cubes and not is_air_pocket((x + 1, y, z)):
            res += 1
        if (x, y - 1, z) not in cubes and not is_air_pocket((x, y - 1, z)):
            res += 1
        if (x, y + 1, z) not in cubes and not is_air_pocket((x, y + 1, z)):
            res += 1
        if (x, y, z - 1) not in cubes and not is_air_pocket((x, y, z - 1)):
            res += 1
        if (x, y, z + 1) not in cubes and not is_air_pocket((x, y, z + 1)):
            res += 1
    return res


print(surface_area(cubes))
