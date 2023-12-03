import re
from dataclasses import dataclass


@dataclass
class NumberSpace:
    line_number: int
    start_index: int
    end_index: int
    value: int


@dataclass
class Asterisk:
    line_number: int
    column_index: int


numbers = []
asterisks = []

file = "./03_input.txt"

with open(file) as f:
    data = f.read().splitlines()

number_pattern = r"\d+"
special_character_pattern = r"[^.\d]"
asterisk_pattern = r"\*"

# Part 1
part_number_sum = 0
for line_number, line in enumerate(data):
    for match in re.finditer(number_pattern, line):
        start_index = match.start()
        end_index = match.end()

        number = int(line[start_index:end_index])
        number_space = NumberSpace(line_number, start_index, end_index - 1, number)
        numbers.append(number_space)

        search_span_start = max(start_index - 1, 0)
        search_span_end = min(end_index + 1, len(line) - 1)

        lines_to_search = [min(max(line_number + i, 0), len(data) - 1) for i in [-1, 0, 1]]
        matches = []
        for line_index in lines_to_search:
            search_content = data[line_index][search_span_start:search_span_end]
            finds = re.findall(special_character_pattern, search_content)
            matches.extend(finds)

        if len(matches):
            part_number_sum += number

    for match in re.finditer(asterisk_pattern, line):
        asterisk = Asterisk(line_number, match.start())
        asterisks.append(asterisk)

# Part 2
total_gear_ratio = 0
for asterisk in asterisks:
    line_number = asterisk.line_number
    column = asterisk.column_index
    search_span_start = max(column - 1, 0)
    search_span_end = min(column + 1, len(data[line_number]) - 1)
    search_range = range(search_span_start, search_span_end + 1)
    lines_to_search = [min(max(line_number + i, 0), len(data) - 1) for i in [-1, 0, 1]]

    match_numbers = []
    for number in numbers:
        column_hit = number.start_index in search_range or number.end_index in search_range
        line_hit = number.line_number in lines_to_search
        if column_hit and line_hit:
            match_numbers.append(number.value)

    if len(match_numbers) == 2:
        gear_ratio = match_numbers[0] * match_numbers[1]
        total_gear_ratio += gear_ratio

print(f"{part_number_sum=}")
print(f"{total_gear_ratio=}")
