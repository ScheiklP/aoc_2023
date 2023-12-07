file = "./06_input.txt"

with open(file) as f:
    data = f.readlines()


def get_num_winning_combinations(race_duration: int, race_distance: int) -> int:
    hold_down_times = range(0, race_duration + 1)
    boat_speeds = hold_down_times
    distances = [(race_duration - hold_down_times[i]) * boat_speeds[i] for i in range(len(hold_down_times))]

    num_winning_combinations = len(list(filter(lambda x: x > race_distance, distances)))

    return num_winning_combinations


race_durations = [int(x) for x in filter(len, data[0].split(":")[1].strip(" ").replace("\n", "").split(" "))]
race_distances = [int(x) for x in filter(len, data[1].split(":")[1].strip(" ").replace("\n", "").split(" "))]

race_duration_part2 = int(data[0].replace(" ", "").split(":")[1])
race_distance_part2 = int(data[1].replace(" ", "").split(":")[1])

part1_product = 1
for race_duration, race_distance in zip(race_durations, race_distances):
    part1_product *= get_num_winning_combinations(race_duration, race_distance)
print(f"Part 1: {part1_product}")

part2_product = get_num_winning_combinations(race_duration_part2, race_distance_part2)
print(f"Part 2: {part2_product}")
