import re

# Sample input data (truncated for brevity)
data = """
bxk log out pkt pts: 0
bxk log out pkt pts: 0.033333
bxk log out pkt pts: 0.066666
bxk log out pkt pts: 0.1
bxk log out pkt pts: 0.133333
bxk log out pkt pts: 0.166666
bxk log out pkt pts: 0.2
bxk log out pkt pts: 0.233333
bxk log out pkt pts: 0.266666
bxk log out pkt pts: 0.3
bxk log out pkt pts: 0.333333
bxk log out pkt pts: 0.366666
bxk log out pkt pts: 0.4
bxk log out pkt pts: 0.433333
bxk log out pkt pts: 0.466666
bxk log out pkt pts: 0.5
bxk log out pkt pts: 0.533333
bxk log out pkt pts: 0.566666
bxk log out pkt pts: 0.6
bxk log out pkt pts: 0.633333
bxk log out pkt pts: 0.666666
bxk log out pkt pts: 0.7
bxk log out pkt pts: 0.733333
bxk log out pkt pts: 0.766666
bxk log out pkt pts: 0.8
bxk log out pkt pts: 0.833333
bxk log out pkt pts: 0.866666
bxk log out pkt pts: 0.9
bxk log out pkt pts: 0.933333
bxk log out pkt pts: 0.966666
bxk log out pkt pts: 0
bxk log out pkt pts: 0.033333
bxk log out pkt pts: 0.066666
bxk log out pkt pts: 0.1
bxk log out pkt pts: 0.133333
bxk log out pkt pts: 0.166666
bxk log out pkt pts: 0.2
bxk log out pkt pts: 0.233333
bxk log out pkt pts: 0.266666
bxk log out pkt pts: 0.3
bxk log out pkt pts: 0.333333
bxk log out pkt pts: 0.366666
bxk log out pkt pts: 0.4
bxk log out pkt pts: 0.433333
bxk log out pkt pts: 0.466666
bxk log out pkt pts: 0.5
bxk log out pkt pts: 0.533333
bxk log out pkt pts: 0.566666
bxk log out pkt pts: 0.6
bxk log out pkt pts: 0.633333
bxk log out pkt pts: 0.666666
bxk log out pkt pts: 0.7
bxk log out pkt pts: 0.733333
bxk log out pkt pts: 0.766666
bxk log out pkt pts: 0.8
bxk log out pkt pts: 0.833333
bxk log out pkt pts: 0.866666
bxk log out pkt pts: 0.9
bxk log out pkt pts: 0.933333
bxk log out pkt pts: 0.966666
bxk log out pkt pts: 0
bxk log out pkt pts: 0.033333
bxk log out pkt pts: 0.066666
bxk log out pkt pts: 0.1
bxk log out pkt pts: 0.133333
bxk log out pkt pts: 0.166666
bxk log out pkt pts: 0.2
bxk log out pkt pts: 0.233333
bxk log out pkt pts: 0.266666
bxk log out pkt pts: 0.3
bxk log out pkt pts: 0.333333
bxk log out pkt pts: 0.366666
bxk log out pkt pts: 0.4
bxk log out pkt pts: 0.433333
bxk log out pkt pts: 0.466666
bxk log out pkt pts: 0.5
bxk log out pkt pts: 0.533333
bxk log out pkt pts: 0.566666
bxk log out pkt pts: 0.6
bxk log out pkt pts: 0.633333
bxk log out pkt pts: 0.666666
bxk log out pkt pts: 0.7
bxk log out pkt pts: 0.733333
bxk log out pkt pts: 0.766666
bxk log out pkt pts: 0.8
bxk log out pkt pts: 0.833333
bxk log out pkt pts: 0.866666
bxk log out pkt pts: 0.9
bxk log out pkt pts: 0.933333
bxk log out pkt pts: 0.966666
bxk log out pkt pts: 0
bxk log out pkt pts: 0.033566
bxk log out pkt pts: 0.067133
bxk log out pkt pts: 0.1007
bxk log out pkt pts: 0.134266
bxk log out pkt pts: 0.167833
bxk log out pkt pts: 0.2014
bxk log out pkt pts: 0.234966
bxk log out pkt pts: 0.268533
bxk log out pkt pts: 0.3021
bxk log out pkt pts: 0.335666
bxk log out pkt pts: 0.369233
bxk log out pkt pts: 0.4028
bxk log out pkt pts: 0.436366
bxk log out pkt pts: 0.469933
"""

# Extract all pts values using regular expression
pts_pattern = re.compile(r'bxk log out pkt pts: ([\d\.]+)')

# Find all matches (which will be returned as strings)
pts_values = pts_pattern.findall(data)

# Split the list of pts values in half (we assume the two lists are of equal length)
half = len(pts_values) // 2
first_group = [float(pts) for pts in pts_values[:half]]
second_group = [float(pts) for pts in pts_values[half:]]

# Calculate the differences between corresponding values from the two groups
differences = [second - first for first, second in zip(first_group, second_group)]

# Print the differences
for i, diff in enumerate(differences):
    print(f"Difference between line {i+1}: {diff:.6f}")