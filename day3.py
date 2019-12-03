import inputProcessor as iP

def distance_to_origin(element):
    return abs(element[0]) + abs(element[1])

paths = iP.dump_list_newline("day3")

locations = []

# First we check all locations travelled by the wires
for i in range(0,len(paths)):
    currentpath = paths[i].split(",")
    nl = [(0,0)]
    locations.append(nl)
    lastcoord = (0,0)
    for c in currentpath:
        #RXXXX, LXXXX, UXXX, DXXXX where XXXX is the quantity
        direction = c[0]
        quantity = int(c[1:])
        if direction == 'R':
            for j in range(0,quantity):
                n = (lastcoord[0] + 1, lastcoord[1])
                locations[i].append(n)
                lastcoord = n
        if direction == 'L':
            for j in range(0,quantity):
                n = (lastcoord[0] - 1, lastcoord[1])
                locations[i].append(n)
                lastcoord = n
        if direction == 'U':
            for j in range(0, quantity):
                n = (lastcoord[0], lastcoord[1] + 1)
                locations[i].append(n)
                lastcoord = n
        if direction == 'D':
            for j in range(0, quantity):
                n = (lastcoord[0], lastcoord[1] - 1)
                locations[i].append(n)
                lastcoord = n

original = locations.copy()

# Remove repeated elements
locations[0] = list(dict.fromkeys(locations[0]))
locations[1] = list(dict.fromkeys(locations[1]))

# Remove (0,0)
locations[0].pop(0)
locations[1].pop(0)

# Sort by distance to origin
locations[0].sort(key=distance_to_origin)
locations[1].sort(key=distance_to_origin)

# List of all intersections
intersections = list(set(locations[0]).intersection(locations[1]))

# Note that this would only be correct for a sorted locations or a sorted intersections
print("Closest intersection: ", abs(intersections[0][0]) + abs(intersections[0][1]))

# The position of each element on the original list tells us the number of steps needed to
# reach that position. We just need to find which element of intersections has the
# lowest combined count for both wires

minimum = 9999999999999999999999999999

for x in intersections:
    steps = original[0].index(x) + original[1].index(x)
    if steps < minimum:
        minimum = steps

print("Fewer steps: ", minimum)
