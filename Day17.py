from typing import List, Tuple

with open('Day17.txt') as f:
    out = f.read().rstrip()


class CustomSet(set):
    def add(self, element) -> None:
        if element in self:
            raise Exception("Element found")
        super().add(element)


cave = CustomSet()
curr_top = 5

rock0 = [
    [1, 1, 1, 1]
]

rock1 = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]
rock2 = [
    [0, 0, 1],
    [0, 0, 1],
    [1, 1, 1]
]
rock3 = [
    [1],
    [1],
    [1],
    [1]
]
rock4 = [
    [1, 1],
    [1, 1]
]
rocks = [rock0, rock1, rock2, rock3, rock4]


class Rock:
    def __init__(self, ind: int, start_height: int):
        self.rock = rocks[ind % len(rocks)]
        self.pos = (2, start_height)

    def push_rock(self, _dir: str):
        x, y = self.pos
        if _dir == '>':
            temp = x+1
        else:
            temp = x-1
        if temp < 0 or temp + len(self.rock[0]) - 1 >= 7:
            return
        for i in range(len(self.rock)):
            for j in range(len(self.rock[0])):
                if (i+temp, j+y) in cave:
                    return
        self.pos = (temp, y)

    def fall(self) -> bool:
        x, y = self.pos
        temp = y-1
        if temp - len(self.rock) < 0:
            return False
        for i in range(len(self.rock)):
            for j in range(len(self.rock[0])):
                if (i + x, j + temp) in cave:
                    return False
        self.pos = (x, temp)
        return True

    def add_to_cave(self):
        x, y = self.pos
        for i in range(len(self.rock)):
            for j in range(len(self.rock[0])):
                cave.add((i + x, j + y))


for i in range(2022):
    start_pos = 5
    falling_rock = Rock(i, start_pos)

    while True:
        push_dir = out[i % len(out)]
        falling_rock.push_rock(push_dir)
        if not falling_rock.fall():
            falling_rock.add_to_cave()
            start_pos = falling_rock.pos[1] + 5
            break

