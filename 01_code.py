file = "./01_input.txt"

name_lookup = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e",
}


def process_line(line: str) -> int:
    digits = list(filter(lambda x: x.isdigit(), line))

    first = digits[0]
    last = digits[-1]

    return int(first + last)


with open(file) as f:
    data = f.read().splitlines()


sum_part1 = 0
sum_part2 = 0
for line in data:
    sum_part1 += process_line(line)

    for key, val in name_lookup.items():
        line = line.replace(key, val)

    sum_part2 += process_line(line)

print(f"Part 1: {sum_part1}")
print(f"Part 2: {sum_part2}")
