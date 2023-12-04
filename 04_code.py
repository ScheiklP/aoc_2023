import re
from dataclasses import dataclass

file = "./04_input.txt"

with open(file) as f:
    data = f.readlines()

card_pattern = r"^Card([\s\d])+: ([\d\s]+) \| ([\d\s]+)\n"

points_part1 = 0
num_cards_part2 = 0


@dataclass
class Card:
    card_number: int
    num_winning_numbers: int
    num_instances: int


cards = []

for line in data:
    card_number, winning_numbers, actual_numbers = re.search(card_pattern, line).groups()
    card_number = int(card_number)
    winning_numbers = [int(winning_numbers[i : i + 3]) for i in range(0, len(winning_numbers), 3)]
    actual_numbers = [int(actual_numbers[i : i + 3]) for i in range(0, len(actual_numbers), 3)]

    matches = list(filter(lambda x: x in winning_numbers, actual_numbers))
    num_matches = len(matches)

    cards.append(Card(card_number, num_matches, 1))

    if num_matches > 0:
        points = 2 ** (num_matches - 1)
    else:
        points = 0

    points_part1 += points

for i, card in enumerate(cards):
    wins = card.num_winning_numbers
    num_cards_part2 += card.num_instances

    for following_card in cards[i + 1 : i + 1 + wins]:
        following_card.num_instances += card.num_instances

print(f"Points part 1: {points_part1}")
print(f"Number of cards part 2: {num_cards_part2}")
