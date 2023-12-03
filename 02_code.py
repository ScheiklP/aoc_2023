import re
from functools import reduce

file = "./02_input.txt"

configuration = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

game_id_pattern = r"Game (\d+):"

with open(file) as f:
    data = f.read().splitlines()

sum_part1 = 0
sum_part2 = 0

for line in data:
    game_id = int(re.search(game_id_pattern, line).groups()[0])
    game_content = {color: [] for color in configuration.keys()}

    sets = line.split(":")[1].split(";")
    set_contents = [set.split(",") for set in sets]
    for i in range(len(set_contents)):
        set_contents[i] = [draw.strip(" ").rstrip(" ").split(" ") for draw in set_contents[i]]

    # Part 1
    set_possible = [True] * len(set_contents)
    for set_i, set in enumerate(set_contents):
        draw_possible = [True] * len(set)
        set_dict = {color: int(number) for number, color in set}
        for draw_i, (number, color) in enumerate(set):
            draw_possible[draw_i] = configuration[color] >= int(number)

        set_possible[set_i] = all(draw_possible)
    game_possible = all(set_possible)
    if game_possible:
        sum_part1 += game_id

    # Part 2
    for set in set_contents:
        for number, color in set:
            game_content[color].append(int(number))

    minimal_game_configuration = {color: max(numbers) for color, numbers in game_content.items()}
    game_power = reduce(lambda x, y: x * y, minimal_game_configuration.values())
    sum_part2 += game_power

print(f"Part 1: {sum_part1}")
print(f"Part 2: {sum_part2}")
