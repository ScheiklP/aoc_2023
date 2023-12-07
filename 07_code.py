from collections import defaultdict
from dataclasses import dataclass

file = "./07_input.txt"


@dataclass
class Hand:
    cards: str
    bid: int
    strength: int
    cards_number: int


def counts_to_strength(count_values: list[int]) -> int:
    if count_values[-1] == 5:
        strength = 6
    elif count_values[-1] == 4:
        strength = 5
    elif count_values[-1] == 3:
        if count_values[-2] == 2:
            strength = 4
        else:
            strength = 3
    elif count_values[-1] == 2:
        if count_values[-2] == 2:
            strength = 2
        else:
            strength = 1
    else:
        strength = 0

    return strength


def total_winnings(hand_strengths: dict[int, list[Hand]]) -> int:
    for strength, draws in hand_strengths.items():
        hand_strengths[strength] = sorted(draws, key=lambda x: x.cards_number)

    ranks = []
    for strength, draws in hand_strengths.items():
        for draw in draws:
            ranks.append(draw)

    return sum([card.bid * (i + 1) for i, card in enumerate(ranks)])


with open(file) as f:
    data = f.readlines()

card_order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
card_weight = {card: str(len(card_order) - i).zfill(2) for i, card in enumerate(card_order)}

card_order_part2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
card_weight_part2 = {card: str(len(card_order_part2) - i).zfill(2) for i, card in enumerate(card_order_part2)}

hand_strengths = {strength: [] for strength in range(7)}
hand_strengths_part2 = {strength: [] for strength in range(7)}

for line in data:
    cards, bid = line.split(" ")
    bid = int(bid)
    counts = defaultdict(int)

    cards_number = ""
    cards_number_part2 = ""
    for card in cards:
        counts[card] += 1
        cards_number += card_weight[card]
        cards_number_part2 += card_weight_part2[card]

    count_values = list(counts.values())
    count_values.sort()

    counts_without_j = {card: count for card, count in counts.items() if card != "J"}
    count_values_part2 = list(counts_without_j.values())
    count_values_part2.sort()

    # Edge case of 5 Js
    if len(count_values_part2) == 0:
        count_values_part2 = [counts.get("J", 0)]
    else:
        count_values_part2[-1] = count_values_part2[-1] + counts.get("J", 0)

    strength = counts_to_strength(count_values)
    strength_part2 = counts_to_strength(count_values_part2)

    hand = Hand(cards, bid, strength, int(cards_number))
    hand_part2 = Hand(cards, bid, strength_part2, int(cards_number_part2))

    hand_strengths[strength].append(hand)
    hand_strengths_part2[strength_part2].append(hand_part2)


print(f"Total winnings part 1: {total_winnings(hand_strengths)}")
print(f"Total winnings part 2: {total_winnings(hand_strengths_part2)}")
