import inputProcessor as iP

def new_velocity(a, b):
    if a > b:
        return -1
    elif a < b:
        return 1
    else:
        return 0

def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def abs_sum(tup):
    return abs(tup[0]) + abs(tup[1]) + abs(tup[2])

inpt = iP.dump_list_newline("day12")
inpt = inpt[0:len(inpt) - 1]

position = []
velocity = [(0,0,0),(0,0,0),(0,0,0),(0,0,0)]

for i in inpt:
    values = i.split(",")
    x = int(values[0][3:].replace("<",""))
    y = int(values[1][3:])
    z = int(values[2][3:].replace(">",""))
    position.append((x,y,z))

original_position = position.copy()

steps = int(input("Steps: "))

print("STEP 0")
for i in range(0,4):
    print("pos: <x=", position[i][0], ", y=", position[i][1], ", z=", position[i][2], ">", " vel: <x=", velocity[i][0], ", y=", velocity[i][1], ", z=", velocity[i][2], ">")
print("-----------------------------")
for step in range(0, steps):
    # New velocity
    for i in range(0,4):
        for j in range(0,4):
            if i != j:
                x = velocity[i][0] + new_velocity(position[i][0], position[j][0])
                y = velocity[i][1] + new_velocity(position[i][1], position[j][1])
                z = velocity[i][2] + new_velocity(position[i][2], position[j][2])

                velocity[i] = (x,y,z)
    
    # New position
    for i in range(0,4):
        position[i] = add(position[i],velocity[i]) 

    print("STEP ", step + 1)
    for i in range(0,4):
        print("pos: <x=", position[i][0], ", y=", position[i][1], ", z=", position[i][2], ">", " vel: <x=", velocity[i][0], ", y=", velocity[i][1], ", z=", velocity[i][2], ">")
    print("-----------------------------")


total = 0
for i in range(0, 4):
    potential = abs_sum(position[i])
    kinetic = abs_sum(velocity[i])
    total = total + (potential * kinetic)

print("Total energy: ", total)

position = original_position
velocity = [(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
hashes = []

steps = 0
while True:
    # New velocity
    for i in range(0,4):
        for j in range(0,4):
            if i != j:
                x = velocity[i][0] + new_velocity(position[i][0], position[j][0])
                y = velocity[i][1] + new_velocity(position[i][1], position[j][1])
                z = velocity[i][2] + new_velocity(position[i][2], position[j][2])

                velocity[i] = (x,y,z)
    
    # New position
    for i in range(0,4):
        position[i] = add(position[i],velocity[i]) 
    
    steps = steps + 1

    h = (hash(tuple(position)),hash(tuple(velocity)))
    if h in hashes:
        break
    else:
        hashes.append(h)

print("Steps to return to previous state: ", steps)