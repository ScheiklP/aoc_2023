from functools import cache


@cache
def combinations(signs: str, numbers: tuple) -> int:
    # No more signs
    if len(signs) == 0:
        # No more numbers
        if len(numbers) == 0:
            return 1  # -> valid
        else:
            return 0  # -> invalid

    # No more numbers
    if len(numbers) == 0:
        # Still broken springs
        if "#" in signs:
            return 0  # -> invalid
        else:
            return 1  # -> valid

    sum = 0
    first_character = signs[0]

    # The signs begin with a dot or a maybe-dot
    if first_character in [".", "?"]:
        sum += combinations(signs[1:], numbers)

    # The signs begin with a # or a maybe-#
    if first_character in ["#", "?"]:
        n = numbers[0]
        num_signs = len(signs)
        # For number n
        # At least n signs
        # No dot in the first n signs -> only # or ?
        # Either exactly n signs or the (n+1)-the sign a #
        if n <= num_signs and "." not in signs[:n] and (n == num_signs or signs[n] != "#"):
            # The first n signs are occupied by n, followed by a dot to separate it from the next number
            sum += combinations(signs[n + 1 :], numbers[1:])

    return sum


file = "./12_input.txt"

total_combinations_part1 = 0
total_combinations_part2 = 0
with open(file) as f:
    for line in f.readlines():
        signs, numbers = line.split(" ")
        numbers = tuple(int(num) for num in numbers.split(","))
        total_combinations_part1 += combinations(signs, numbers)

        signs = "?".join([signs] * 5)
        numbers = numbers * 5
        total_combinations_part2 += combinations(signs, numbers)

print(f"Total combinations part 1: {total_combinations_part1}")
print(f"Total combinations part 2: {total_combinations_part2}")
