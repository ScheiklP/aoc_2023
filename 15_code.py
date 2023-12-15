from functools import reduce
from collections import defaultdict


def hash_function(string):
    current_value = 0
    for character in string:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256
    return current_value


file = "15_input.txt"

with open(file) as f:
    sequence = f.readline().rstrip("\n").split(",")

sequence_value = reduce(lambda x, y: x + hash_function(y), sequence, 0)

print(f"Total sum part 1: {sequence_value}")


box_buffer = defaultdict(list)

for step in sequence:
    dash_operation = step[-1] == "-"
    lens_label = step[:-1] if dash_operation else step.split("=")[0]
    box = hash_function(lens_label)
    box_contents = box_buffer[box]
    lens_label_matches = list(filter(lambda x: lens_label in x, box_contents))
    assert len(lens_label_matches) < 2

    if dash_operation:
        if len(lens_label_matches):
            box_contents.remove(lens_label_matches[0])
    else:
        focal_length = step[-1]
        lens = lens_label + " " + focal_length
        if len(lens_label_matches):
            lens_index = box_contents.index(lens_label_matches[0])
            box_contents[lens_index] = lens
        else:
            box_buffer[box].append(lens)


total_focusing_power = 0
for box_number, box_contents in box_buffer.items():
    for slot_number, lens in enumerate(box_contents):
        focusing_power = (1 + box_number) * (1 + slot_number) * int(lens.split(" ")[-1])
        total_focusing_power += focusing_power

print(f"Total focusing part 2: {total_focusing_power}")
