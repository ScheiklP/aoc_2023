from copy import deepcopy
from collections import defaultdict

file = "14_input.txt"

with open(file) as f:
    rows = [line.rstrip("\n") for line in f.readlines()]


def full_shift(rows):
    columns = [list(x) for x in zip(*rows)]
    for column in columns:
        reached_end = False
        row_i = 0
        while not reached_end:
            character = column[row_i]
            if character in "#O":
                row_i += 1
            elif character == ".":
                tail = column[row_i + 1 :]
                if tail.count("O") == 0:
                    break
                for next_i, next_character in enumerate(tail):
                    if next_character == ".":
                        pass
                    elif next_character == "O":
                        column[row_i] = "O"
                        column[row_i + next_i + 1] = "."
                        row_i += 1
                        break
                    elif next_character == "#":
                        row_i += next_i + 1
                        break
            reached_end = row_i >= len(column) - 1

    return ["".join(list(x)) for x in zip(*columns)]


def full_cycle(rows):
    # Tilt north
    rows = full_shift(rows)

    # Tilt west
    rows = list(["".join(list(x)) for x in zip(*rows)])
    rows = full_shift(rows)

    # Tilt south
    rows = list(reversed(["".join(list(x)) for x in zip(*rows)]))
    rows = full_shift(rows)

    # Tilt east
    rows = list(reversed(["".join(list(x)) for x in zip(*rows)]))
    rows = full_shift(rows)

    return list(reversed(["".join(list(x)) for x in zip(*reversed(rows))]))


def get_weight(rows):
    total_weight = 0
    for i, row in enumerate(rows):
        row_weight = (len(rows) - i) * row.count("O")
        total_weight += row_weight
    return total_weight


rows_part_1 = deepcopy(rows)
print("Total weight part 1: ", get_weight(full_shift(rows_part_1)))

num_cycles = 1000000000
done_cycles = 0
loop_start = 0
loop_end = 0
index_buffer = defaultdict(list)
while True:
    rows = full_cycle(rows)
    hashable_rows = "".join(rows)
    if hashable_rows in index_buffer:
        loop_start = index_buffer[hashable_rows][0]
        loop_end = done_cycles
        break
    else:
        index_buffer[hashable_rows].append(done_cycles)
    done_cycles += 1
remaining_cycles = (num_cycles - loop_start) % (loop_end - loop_start) - 1
for i in range(remaining_cycles):
    rows = full_cycle(rows)
print("Total weight part 2: ", get_weight(rows))
