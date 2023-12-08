import re
import math

file = "08_input.txt"
map_pattern = r"([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)"
first_node = "AAA"
maps = {}

with open(file) as f:
    data = f.readlines()

instructions = [0 if instruction == "L" else 1 for instruction in data[0].rstrip("\n")]

start_nodes = []
for line in data[2:]:
    node, left, right = re.search(map_pattern, line).groups()
    maps[node] = (left, right)
    if node.endswith("A"):
        start_nodes.append(node)

# Part 1
reached_end = False
num_steps = 0
current_node = first_node

while not reached_end:
    for instruction in instructions:
        current_node = maps[current_node][instruction]
        num_steps += 1
        reached_end = current_node == "ZZZ"

print(f"Number of steps Part 1: {num_steps}")

# Part 2
num_steps = 0
current_nodes = start_nodes.copy()
terminal_node_steps = [[] for _ in range(len(current_nodes))]

# Get a few data points for how often each starting node meets a terminal state
while not all([len(steps) > 4 for steps in terminal_node_steps]):
    for instruction in instructions:
        for node_idx, node in enumerate(current_nodes):
            current_nodes[node_idx] = maps[node][instruction]
        num_steps += 1

        terminal_nodes = [node.endswith("Z") for node in current_nodes]
        for index, terminal in enumerate(terminal_nodes):
            if terminal:
                terminal_node_steps[index].append(num_steps)

# Get the distances between terminal nodes for each starting node
terminal_node_distances = []
for step_list in terminal_node_steps:
    distances = [step_list[i] - step_list[i - 1] for i in range(1, len(step_list))]
    assert all([distance == distances[0] for distance in distances])
    terminal_node_distances.append(distances[0])

# The least common multiplier of step distances is where the nodes meet in final nodes
print(f"Number of steps Part 2: {math.lcm(*terminal_node_distances)}")
