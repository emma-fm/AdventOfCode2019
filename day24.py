import inputProcessor as iP

def adjacent_bugs(bugs, coords):
    adj = 0
    if (coords[0] + 1,coords[1]) in bugs:
        adj = adj + 1
    if (coords[0] - 1, coords[1]) in bugs:
        adj = adj + 1
    if (coords[0], coords[1] + 1) in bugs:
        adj = adj + 1
    if (coords[0], coords[1] - 1) in bugs:
        adj = adj + 1
    return adj

initial_state = iP.dump_list_newline("day24")[:-1]

def sortkey(e):
    return e[0] + 5*e[1]

def print_layout(bugs, spaces):
    comb = []
    for b in bugs:
        comb.append((b[0],b[1],"#"))
    for s in spaces:
        comb.append((s[0],s[1],"."))
    
    list.sort(comb, key=sortkey)

    prevy = 0
    print("")
    for c in comb:
        if c[1] > prevy:
            print("")
            prevy = c[1]
        if c[2] == "#":
            print("#",end="")
        elif c[2] == ".":
            print(".",end="")


bugs = []
spaces = []
x = 0
y = 0
for l in initial_state:
    for s in l:
        if s == "#":
            bugs.append((x,y))
        elif s == ".":
            spaces.append((x,y))
        x = x + 1
    x = 0
    y = y + 1


previous_layouts = []
previous_layouts.append(bugs.copy())

new_bugs = bugs.copy()
new_spaces = spaces.copy()

while True:
    for b in bugs:
        # Dies?
        if adjacent_bugs(bugs, b) != 1:
            new_bugs.remove(b)
            new_spaces.append(b)

    for s in spaces:
        # Infest?
        if adjacent_bugs(bugs, s) == 1 or adjacent_bugs(bugs, s) == 2:
            new_spaces.remove(s)
            new_bugs.append(s)

    bugs = new_bugs.copy()
    spaces = new_spaces.copy()
    list.sort(bugs)
    list.sort(spaces)
    if bugs in previous_layouts:
        break
    else:
        previous_layouts.append(bugs.copy())

print_layout(bugs, spaces)

# Biodiversity rating:
bio = 0
for b in bugs:
    bio = bio + pow(2, 5 * b[1] + b[0])

print("\nBiodiversity rating: ", bio)