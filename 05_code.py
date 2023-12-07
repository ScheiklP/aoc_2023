import re
from dataclasses import dataclass, field
from multiprocessing import Pool


@dataclass
class Map:
    source: str
    destination: str
    source_ranges: list[range] = field(default_factory=list[range])
    destination_ranges: list[range] = field(default_factory=list[range])


MAPS = {}


def seed_to_destination(seed) -> int:
    destination_value = seed
    for map in MAPS.values():
        source_index = None
        for item_index, source_range in enumerate(map.source_ranges):
            if destination_value >= source_range.start and destination_value < source_range.stop:
                source_index = destination_value - source_range.start
                range_index = item_index
                break

        if source_index == None:
            destination_value = destination_value
        else:
            destination_value = map.destination_ranges[range_index].start + source_index

    return destination_value


file = "./05_input.txt"

map_name_pattern = r"([a-z]+)-to-([a-z]+) map:"
empty_line_pattern = r"^\s$"

with open(file) as f:
    data = f.readlines()


map_names = list(filter(lambda x: "map" in x, data))

current_map = None
for i, line in enumerate(data):
    if i == 0:
        seeds = [int(x.replace("\n", "")) for x in line.split("seeds: ")[1].split(" ")]
        seed_ranges_part2 = [range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
        continue
    elif re.search(empty_line_pattern, line) is not None:
        continue
    elif "map" in line:
        source_name, destination_name = re.search(map_name_pattern, line).groups()
        current_map = Map(source=source_name, destination=destination_name)
        # source_destination_pairs.append((source_name, destination_name))
        MAPS[(source_name, destination_name)] = current_map
    else:
        assert current_map is not None

        destination_range_start, source_range_start, range_length = [int(x) for x in line.replace("\n", "").split(" ")]

        current_map.source_ranges.append(range(source_range_start, source_range_start + range_length))
        current_map.destination_ranges.append(range(destination_range_start, destination_range_start + range_length))


destination_values = []
for seed in seeds:
    destination_value = seed_to_destination(seed)

    destination_values.append(destination_value)

print(f"Min destination value: {min(destination_values)}")


min_destination_value = 2**64
for seed_range in seed_ranges_part2:
    seeds = list(seed_range)

    with Pool(25) as pool:
        destination_values = pool.map(seed_to_destination, seeds)

    min_destination_value = min(min_destination_value, min(destination_values))

print(f"Min destination value: {min_destination_value}")
