from functools import reduce

file = "./09_input.txt"

with open(file) as f:
    data = [list(map(int, line.rstrip("\n").split(" "))) for line in f.readlines()]

new_values = []
previous_values = []

for sequence in data:
    current_sequence = sequence
    reached_all_zeros = False
    final_values = []
    initial_values = []

    while not reached_all_zeros:
        final_values.append(current_sequence[-1])
        initial_values.append(current_sequence[0])

        diff_list = [current_sequence[i] - current_sequence[i - 1] for i in range(1, len(current_sequence))]
        reached_all_zeros = all([val == 0 for val in diff_list])
        current_sequence = diff_list

    final_values.reverse()
    new_values.append(reduce(lambda x, y: x + y, final_values, 0))

    initial_values.reverse()
    previous_values.append(reduce(lambda x, y: y - x, initial_values, 0))

print(f"Sum of new values Part 1: {sum(new_values)}")
print(f"Sum of new values Part 2: {sum(previous_values)}")
