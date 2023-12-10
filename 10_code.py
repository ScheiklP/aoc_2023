from enum import Enum
from functools import reduce


class Direction(Enum):
    NORTH = 0
    WEST = 1
    EAST = 2
    SOUTH = 3


def get_opposite_direction(direction: Direction) -> Direction:
    if direction == Direction.NORTH:
        return Direction.SOUTH
    elif direction == Direction.SOUTH:
        return Direction.NORTH
    elif direction == Direction.WEST:
        return Direction.EAST
    elif direction == Direction.EAST:
        return Direction.WEST


def get_next_indices(indices: tuple[int, int], direction: Direction) -> tuple[int, int]:
    current_row, current_column = indices
    next_row, next_column = None, None

    if direction == Direction.NORTH:
        next_row = current_row - 1
        next_column = current_column
    elif direction == Direction.WEST:
        next_row = current_row
        next_column = current_column - 1
    elif direction == Direction.SOUTH:
        next_row = current_row + 1
        next_column = current_column
    else:
        next_row = current_row
        next_column = current_column + 1

    return next_row, next_column


def get_valid_next_characters(direction: Direction) -> list[str]:
    if direction == Direction.NORTH:
        return ["|", "7", "F"]
    elif direction == Direction.WEST:
        return ["-", "F", "L"]
    elif direction == Direction.SOUTH:
        return ["|", "J", "L"]
    else:
        return ["-", "J", "7"]


def get_next_direction(character: str, origin_direction: Direction) -> Direction | None:
    if origin_direction == Direction.NORTH:
        if character == "|":
            return Direction.SOUTH
        elif character == "L":
            return Direction.EAST
        elif character == "J":
            return Direction.WEST
        else:
            return None

    elif origin_direction == Direction.WEST:
        if character == "-":
            return Direction.EAST
        elif character == "J":
            return Direction.NORTH
        elif character == "7":
            return Direction.SOUTH
        else:
            return None

    elif origin_direction == Direction.SOUTH:
        if character == "|":
            return Direction.NORTH
        elif character == "F":
            return Direction.EAST
        elif character == "7":
            return Direction.WEST
        else:
            return None

    elif origin_direction == Direction.EAST:
        if character == "-":
            return Direction.WEST
        elif character == "F":
            return Direction.SOUTH
        elif character == "L":
            return Direction.NORTH
        else:
            return None
    else:
        raise RuntimeError("Whoopsy")


def test_indices_valid(indices: tuple[int, int], max_indices: tuple[int, int]) -> bool:
    row, column = indices
    max_row, max_column = max_indices
    row_valid = row >= 0 and row <= max_row
    column_valid = column >= 0 and column <= max_column

    return row_valid and column_valid


# file = "10_test_input_part2.txt"
file = "10_input.txt"


with open(file) as f:
    data = [line.rstrip("\n") for line in f.readlines()]

start_row = None
start_column = None
for row, line in enumerate(data):
    for column, character in enumerate(line):
        if character == "S":
            start_row = row
            start_column = column
max_indices = (len(data) - 1, len(line) - 1)


# Get possible starts of the loop
start_indices = []
origin_directions = []
for direction in Direction:
    next_indices = get_next_indices((start_row, start_column), direction)
    indices_valid = test_indices_valid(next_indices, max_indices)
    if not indices_valid:
        pass
    else:
        next_character = data[next_indices[0]][next_indices[1]]
        if next_character in get_valid_next_characters(direction):
            start_indices.append(next_indices)
            origin_directions.append(get_opposite_direction(direction))


# For each possible loop start, try to close the loop
depth_to_s = []
loop_nodes = set()
for current_indices, origin_direction in zip(start_indices, origin_directions):
    current_loop_nodes = [(start_row, start_column)]
    current_depth = 0
    terminal_state = False
    reached_s = False
    while not terminal_state:
        current_character = data[current_indices[0]][current_indices[1]]
        current_depth += 1
        if current_character == "S":
            terminal_state = True
            reached_s = True
            depth_to_s.append(current_depth)
            for node in current_loop_nodes:
                loop_nodes.add(node)
        next_direction = get_next_direction(current_character, origin_direction)
        if next_direction is not None:
            current_loop_nodes.append(current_indices)
            current_indices = get_next_indices(current_indices, next_direction)
            indices_valid = test_indices_valid(current_indices, max_indices)
            if not indices_valid:
                terminal_state = True
            else:
                origin_direction = get_opposite_direction(next_direction)
        else:
            terminal_state = True

assert all([depth == depth_to_s[0] for depth in depth_to_s])
print(f"Farthest steps: {depth_to_s[0] // 2}")

# Replace S with the actual character
maybe_s = [get_valid_next_characters(origin_direction) for origin_direction in origin_directions]
s = list(reduce(lambda x, y: set(x) & set(y), maybe_s))[0]
data[start_row] = data[start_row].replace("S", s)

# Replace all non-loop characters with dots
for row, line in enumerate(data):
    data[row] = [character if (row, column) in loop_nodes else "." for column, character in enumerate(line)]

# Find all nodes that are not within the loop
outside_nodes = []
for row, line in enumerate(data):
    inside = False
    corner_from_north = None
    for column, character in enumerate(line):
        if character == "|":  # crossing a loop border flips the flag
            inside = not inside
        elif character in "LF":  # crossing a corner of the loop. From north for an L, from south for an F
            corner_from_north = character == "L"
        elif character in "7J":  # crossing a corner of the loop. If we came in from the north, and leave to south, flip the flag. Same if we came from south, and leave to north.
            if character != ("J" if corner_from_north else "7"):
                inside = not inside
            corner_from_north = None  # reset the crossing flag
        if not inside:
            outside_nodes.append((row, column))


# Number of inside nodes is total number minos outside and loop nodes
total_number_of_nodes_not_inside = len(set(outside_nodes) | set(loop_nodes))
total_number_of_nodes = len(data) * len(data[0])

print(f"Total number of inside nodes: {total_number_of_nodes - total_number_of_nodes_not_inside}")
