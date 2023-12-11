def manhatten_distance(first: tuple[int, int], second: tuple[int, int]) -> int:
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


file = "11_input.txt"
expansion_factor_part1 = 2
expansion_factor_part2 = 1000000

with open(file) as f:
    data = [line.rstrip("\n") for line in f.readlines()]

# Find galaxies
galaxy_coordinates = []
for i in range(len(data)):
    for j in range(len(data[0])):
        character = data[i][j]
        if character == "#":
            galaxy_coordinates.append((i, j))

# Built possible pairs
galaxy_pairs = []
for galaxy_index, galaxy_coordinate in enumerate(galaxy_coordinates):
    for i in range(galaxy_index + 1, len(galaxy_coordinates)):
        galaxy_pairs.append((galaxy_coordinate, galaxy_coordinates[i]))


# Detect empty rows and columns in the data
empty_row_indices = []
empty_column_indices = []
for row_index, line in enumerate(data):
    empty_row = all([character == "." for character in line])
    if empty_row:
        empty_row_indices.append(row_index)
for i in range(len(data[0])):
    column = []
    for j in range(len(data)):
        column.append(data[j][i])
    empty_column = all([character == "." for character in column])
    if empty_column:
        empty_column_indices.append(i)

# Calculate distances and sum them up
sum_distance_part1 = 0
sum_distance_part2 = 0
for galaxy_pair in galaxy_pairs:
    first, second = galaxy_pair
    min_row = min(first[0], second[0])
    max_row = max(first[0], second[0])
    min_column = min(first[1], second[1])
    max_column = max(first[1], second[1])
    empty_rows_between_pair = sum([(row_index >= min_row) and (row_index <= max_row) for row_index in empty_row_indices])
    empty_columns_between_pair = sum([column_index >= min_column and column_index <= max_column for column_index in empty_column_indices])

    distance = manhatten_distance(first, second)
    distance = distance - empty_rows_between_pair - empty_columns_between_pair
    distance_part1 = distance + (empty_rows_between_pair + empty_columns_between_pair) * expansion_factor_part1
    distance_part2 = distance + (empty_rows_between_pair + empty_columns_between_pair) * expansion_factor_part2
    sum_distance_part1 += distance_part1
    sum_distance_part2 += distance_part2

print(f"Sum of distances part 1: {sum_distance_part1}")
print(f"Sum of distances part 2: {sum_distance_part2}")
