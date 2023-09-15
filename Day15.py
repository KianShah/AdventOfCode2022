from time import perf_counter
from typing import Tuple, List, Dict, Set

with open('Day15.txt') as f:
    out = f.read().split('\n')


def manhatten_dist(A: Tuple[int, int], B: Tuple[int, int]) -> int:
    return abs(A[0] - B[0]) + abs(A[1] - B[1])


# Part 1
print("Part 1")
cannot_contain_beacons: Set[int] = set()
beacons: Set[Tuple[int, int]] = set()
target_row = 2000000

for line in out:
    tokens = line.split(' ')
    s_x, s_y, b_x, b_y = tokens[2], tokens[3], tokens[8], tokens[9]
    s_x = int(s_x[2:-1])
    s_y = int(s_y[2:-1])
    b_x = int(b_x[2:-1])
    b_y = int(b_y[2:])
    dist_to_beacon = manhatten_dist((s_x, s_y), (b_x, b_y))
    dist_to_2mil = abs(s_y - target_row)
    beacons.add((b_x, b_y))
    extra_dist = dist_to_beacon - dist_to_2mil
    if extra_dist > 0:
        for i in range(s_x - extra_dist, s_x + extra_dist + 1):
            cannot_contain_beacons.add(i)

for bx, by in beacons:
    if by == target_row:
        cannot_contain_beacons.remove(bx)
print(len(cannot_contain_beacons))

# Part 2
print("Part 2")


def merge_intervals(intervals):
    # First, sort the intervals by their start times
    intervals = sorted(intervals, key=lambda x: x[0])

    # Initialize the merged intervals with the first interval in the list
    merged = [intervals[0]]

    # Iterate through the rest of the intervals and try to merge them
    # with the last interval in the `merged` list
    for current in intervals[1:]:
        previous = merged[-1]
        # If the current interval overlaps with the previous interval,
        # merge them by updating the end time of the previous interval
        # if the current interval extends past it
        if current[0] <= previous[1]:
            merged[-1] = (previous[0], max(previous[1], current[1]))
        # Otherwise, just append the current interval to the `merged` list
        else:
            merged.append(current)

    return merged


def add_interval(intervals: List[Tuple[int, int]], new_interval: Tuple[int, int]) -> List[Tuple[int, int]]:
    result = []

    i = 0
    while i < len(intervals):
        if intervals[i][1] < new_interval[0]:
            result.append(intervals[i])
        elif new_interval[1] < intervals[i][0]:
            result.append(new_interval)
            result += intervals[i:]
            break
        else:
            new_interval = (min(intervals[i][0], new_interval[0]), max(intervals[i][1], new_interval[1]))
        i += 1

    if i == len(intervals):
        result.append(new_interval)

    return result


sensors: Dict[Tuple[int, int], int] = {}
for line in out:
    tokens = line.split(' ')
    s_x, s_y, b_x, b_y = tokens[2], tokens[3], tokens[8], tokens[9]
    s_x = int(s_x[2:-1])
    s_y = int(s_y[2:-1])
    b_x = int(b_x[2:-1])
    b_y = int(b_y[2:])
    dist_to_beacon = manhatten_dist((s_x, s_y), (b_x, b_y))
    sensors[(s_x, s_y)] = dist_to_beacon

start = perf_counter()
for row in range(4000001):
    invalid_ranges = []
    for sensor, s_range in sensors.items():
        s_x, s_y = sensor
        dist_to_2mil = abs(s_y - row)
        extra_dist = s_range - dist_to_2mil
        if extra_dist > 0:
            new_invalid_range = max(0, s_x - extra_dist), min(4000000, s_x + extra_dist)
            invalid_ranges.append(new_invalid_range)

    invalid_ranges = merge_intervals(invalid_ranges)
    if len(invalid_ranges) != 1 or invalid_ranges[0] != (0, 4000000):
        target_x = invalid_ranges[0][1] + 1
        target_y = row
        print(f"Tuning frequency: {target_x * 4000000 + target_y}")
        print(f"Time taken: {perf_counter() - start} s")
        break
