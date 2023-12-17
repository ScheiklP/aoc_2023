from enum import Enum, auto
from dataclasses import dataclass
from collections import defaultdict


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    WEST = auto()
    EAST = auto()


@dataclass
class Ray:
    row: int
    col: int
    direction: Direction


def direction_to_position(row: int, col: int, direction: Direction) -> [int, int]:
    if direction == Direction.NORTH:
        return row - 1, col
    elif direction == Direction.SOUTH:
        return row + 1, col
    elif direction == Direction.WEST:
        return row, col - 1
    else:
        return row, col + 1


mirrors = {
    "/": {
        Direction.NORTH: Direction.EAST,
        Direction.EAST: Direction.NORTH,
        Direction.WEST: Direction.SOUTH,
        Direction.SOUTH: Direction.WEST,
    },
    "\\": {
        Direction.NORTH: Direction.WEST,
        Direction.WEST: Direction.NORTH,
        Direction.EAST: Direction.SOUTH,
        Direction.SOUTH: Direction.EAST,
    },
}

splitters = {
    "|": {
        Direction.NORTH: Direction.NORTH,
        Direction.SOUTH: Direction.SOUTH,
        Direction.WEST: [Direction.NORTH, Direction.SOUTH],
        Direction.EAST: [Direction.NORTH, Direction.SOUTH],
    },
    "-": {
        Direction.NORTH: [Direction.WEST, Direction.EAST],
        Direction.SOUTH: [Direction.WEST, Direction.EAST],
        Direction.WEST: Direction.WEST,
        Direction.EAST: Direction.EAST,
    },
}

file = "16_input.txt"

with open(file) as f:
    data = [line.rstrip("\n") for line in f.readlines()]

row = 0
col = -1
direction = Direction.EAST

min_row = min_col = 0
max_row = len(data) - 1
max_col = len(data[0]) - 1

left_side = [(i, -1, Direction.EAST) for i in range(0, len(data))]
bottom_side = [(len(data), i, Direction.NORTH) for i in range(0, len(data[0]))]
right_side = [(i, len(data[0]), Direction.WEST) for i in range(0, len(data))]
top_side = [(-1, i, Direction.SOUTH) for i in range(0, len(data[0]))]
starts = left_side + bottom_side + right_side + top_side

max_energized_tiles = 0
for row, col, direction in starts:
    start_row, start_col, start_direction = row, col, direction
    history = defaultdict(list)
    rays = []
    ray = Ray(row=row, col=col, direction=direction)
    rays.append(ray)

    while len(rays):
        row, col = direction_to_position(row, col, direction)

        if (
            min_row > row
            or max_row < row
            or min_col > col
            or max_col < col
        ):
            # Hit a wall
            rays.pop(0)
            if len(rays):
                ray = rays[0]
                row = ray.row
                col = ray.col
                direction = ray.direction
                history[(row, col)].append(direction)
        else:
            next_character = data[row][col]
            if next_character == ".":
                pass
            elif next_character in mirrors:
                direction = mirrors[next_character][direction]
            elif next_character in splitters:
                directions = splitters[next_character][direction]
                if isinstance(directions, list):
                    new_ray = Ray(row=row, col=col, direction=directions[1])
                    rays.append(new_ray)
                    direction = directions[0]
                else:
                    direction = directions

            if direction in history[(row, col)]:
                rays.pop(0)
                if len(rays):
                    ray = rays[0]
                    row = ray.row
                    col = ray.col
                    direction = ray.direction
                    history[(row, col)].append(direction)
            else:
                history[(row, col)].append(direction)
                ray.row = row
                ray.col = col
                ray.direction = direction

    if max_energized_tiles == 0:
        print(f"Energized tiles Part 1: {len(history)}")
    if max_energized_tiles < len(history):
        max_energized_tiles = len(history)
        best_start = (start_row, start_col, start_direction)

print(f"Energized tiles Part 2: {max_energized_tiles}")
