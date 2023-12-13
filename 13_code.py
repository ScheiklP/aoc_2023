def sign_distance(line1, line2) -> int:
    return sum([a != b for a, b in zip(line1, line2)])


def get_mirror_line(lines: list[str], part2: bool = False) -> int | None:
    mirror_line = None
    for i in range(1, len(lines)):
        above = lines[:i]
        below = lines[i:]

        min_num = min([len(above), len(below)])
        if len(above) < len(below):
            compare = reversed(below[:min_num])
            sign_distances = [sign_distance(above_line, below_line) for above_line, below_line in zip(above, compare)]
        else:
            compare = reversed(above[-min_num:])
            sign_distances = [sign_distance(above_line, below_line) for above_line, below_line in zip(compare, below)]

        if part2:
            match = sum(sign_distances) == 1
        else:
            match = sum(sign_distances) == 0

        if match:
            mirror_line = i

    return mirror_line


def print_data(rows, mirror_row, mirror_column):
    num_columns = len(rows[0])

    print_rows = []
    print_rows.append(" " * (num_columns + 2))
    print_rows.extend([" " + row + " " for row in rows])
    print_rows.append(" " * (num_columns + 2))

    if mirror_row is not None:
        print_rows[mirror_row + 1] = "v" + rows[mirror_row] + "v"
        print_rows[mirror_row + 2] = "^" + rows[mirror_row + 1] + "^"

    if mirror_column is not None:
        print_rows[0] = " " * (mirror_column + 1) + ">" + "<"
        print_rows[-1] = " " * (mirror_column + 1) + ">" + "<"

    for row in print_rows:
        print(row)

    print("-------------------------------------------------")


file = "13_input.txt"

data = []
with open(file) as f:
    pattern = []
    for line in f.readlines():
        line = line.rstrip("\n")
        if len(line) == 0:
            data.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    data.append(pattern)


total_sum_part1 = 0
total_sum_part2 = 0

for pattern in data:
    rows = pattern
    columns = ["".join(list(x)) for x in zip(*rows)]

    pattern_sum = 0
    mirror_row = get_mirror_line(rows)
    mirror_column = get_mirror_line(columns)
    if mirror_row is not None:
        pattern_sum += 100 * mirror_row
    if mirror_column is not None:
        pattern_sum += mirror_column
    total_sum_part1 += pattern_sum

    pattern_sum = 0
    mirror_row = get_mirror_line(rows, part2=True)
    mirror_column = get_mirror_line(columns, part2=True)
    if mirror_row is not None:
        pattern_sum += 100 * mirror_row
    if mirror_column is not None:
        pattern_sum += mirror_column
    total_sum_part2 += pattern_sum

    # print_data(rows, mirror_row, mirror_column)


print(f"Total sum part 1: {total_sum_part1}")
print(f"Total sum part 2: {total_sum_part2}")
