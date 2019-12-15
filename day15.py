import inputProcessor as iP
import random

# directions
NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
# status
WALL = 0
EMPTY = 1
OX_SYS = 2
ROBOT = 3

def think_about_walls(zonemap):
    max_y = max([t[1] for t in zonemap])
    min_y = min([t[1] for t in zonemap])

    max_x = max([t[0] for t in zonemap])
    min_x = min([t[0] for t in zonemap])

    for file in reversed(range(min_y, max_y + 1)):
        for column in range(min_x, max_x + 1):
            if not ((column,file,EMPTY) in zonemap or (column,file,WALL) in zonemap or (column,file,OX_SYS) in zonemap or (column,file,ROBOT) in zonemap):
                if (column + 1, file, WALL) in zonemap and (column - 1, file, WALL) in zonemap and (column, file + 1, WALL) in zonemap and (column,file - 1, WALL) in zonemap:
                    zonemap.append((column,file,WALL))

def print_map(zonemap, robotpos):
    zonemap.append((robotpos[0], robotpos[1], ROBOT))
    ox = False
    try:
        zonemap.remove((robotpos[0], robotpos[1], EMPTY))
    except ValueError as ex:
        zonemap.remove((robotpos[0], robotpos[1], OX_SYS))
        ox = True
    
    max_y = max([t[1] for t in zonemap])
    min_y = min([t[1] for t in zonemap])

    max_x = max([t[0] for t in zonemap])
    min_x = min([t[0] for t in zonemap])
    for file in reversed(range(min_y, max_y + 1)):
        for column in range(min_x, max_x + 1):
            if (column,file,EMPTY) in zonemap or (column,file,WALL) in zonemap or (column,file,OX_SYS) in zonemap or (column,file,ROBOT) in zonemap:
                for t in zonemap:
                    if t[0] == column and t[1] == file:
                        char = ""
                        if t[0] == 0 and t[1] == 0:
                            char = "X"
                        elif t[2] == WALL:
                            char = "#"
                        elif t[2] == EMPTY:
                            char = "."
                        elif t[2]== OX_SYS:
                            char = "O"
                        elif t[2] == ROBOT:
                            char = "D"
                        print(char, end="")
                        break
            else:
                print("?", end="")
        print("")
    print("")
    zonemap.remove((robotpos[0], robotpos[1], ROBOT))
    if not ox:
        zonemap.append((robotpos[0], robotpos[1], EMPTY))
    else:
        zonemap.append((robotpos[0], robotpos[1], OX_SYS))

# Allocates quantity values at memory, initialized at 0
def allocate(mem, quantity):
    for i in range(0, quantity + 1):
        mem.append(0)

# Store at the correct memory
def store_at_address(st, mem, pos, value):
    if pos < len(st): # on states
        st[pos] = value
    else: # on memory
        if len(mem) > (pos - len(st)): #fits
            mem[pos - len(st)] = value
        else: # won't fit: allocate and then call method again
            diff = (pos - len(st)) - len(mem)
            allocate(mem, diff)
            store_at_address(st, mem, pos, value)

# Get value from its correct memory
def get_from_address(st, mem, pos):
    if pos < len(st): # on states
        return st[pos]
    else: # on memory
        if len(mem) > (pos - len(st)): #fits
            return mem[pos - len(st)]
        else: #unallocated memory. return 0
            return 0


# st is an INTEGER list!
def calculate(st, mem, inpt, i=0, relative_address=0):
    while i < len(st):
        # Calculate modes
        opcode = st[i]
        mode = [0,0,0]

        if int(st[i] / 10) != 0: # Not length 1
            opcode = st[i] % 100 # 1002 -> 1002 % 100 = 2
            mode[0] = int(st[i] / 100) % 10 # 1002 -> 1002 / 100 = 10 % 10 = 0
            mode[1] = int(st[i] / 1000) % 10 # 1002 -> 1002 / 1000 = 1 % 10 = 1
            mode[2] = int(st[i] / 10000) % 10 # 1002 -> 1002 / 10000 = 0 % 10 = 0
        
        # Calculate quantity of parameters (except return parameter!)
        parameters = []
        if opcode != 3 and opcode != 4 and opcode != 99:
            parameters = [0,0] # two parameters
        elif opcode == 3:
            # Special case. Ask for input.
            parameters = [inpt,0]
        elif opcode == 4:
            # Special case
            parameters = [0]
        elif opcode == 9:
            # Special case
            parameters = [0]

        # Calculate parameters for all opcodes but 3 and 99
        if opcode != 3 and opcode != 99:
            for j in range(0,len(parameters)):
                if mode[j] == 0: # position mode
                    parameters[j] = get_from_address(st, mem, get_from_address(st, mem, i + j + 1))
                elif mode[j] == 1: # immediate mode
                    parameters[j] = get_from_address(st, mem, i + j + 1)
                elif mode[j] == 2: # relative mode
                    parameters[j] = get_from_address(st, mem, relative_address + get_from_address(st, mem, i + j + 1))

        if opcode == 3 and mode[0] == 0:
            parameters[1] =get_from_address(st, mem, i + 1)
        elif opcode == 3 and mode[0] == 2:
            parameters[1] = relative_address + get_from_address(st, mem, i + 1)

        base = 0
        if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
            if mode[2] == 2:
                base = relative_address

        if opcode == 1: # add parameters 0 and 1 and store them at direction pointed by 2
            store_at_address(st, mem, base + get_from_address(st, mem, i + 3), parameters[0] + parameters[1])
            i = i + 4
        elif opcode == 2: # multiply parameters 0 and 2 and store them at direction pointed by 2
            store_at_address(st, mem, base + get_from_address(st, mem, i + 3), parameters[0] * parameters[1])
            i = i + 4
        elif opcode == 3: # Store input at address of parameter 1
            store_at_address(st, mem, parameters[1], parameters[0])
            i = i + 2
        elif opcode == 4: # Return value at address at parameter 0
            i = i + 2
            return (parameters[0], i, relative_address)
        elif opcode == 5: # jump if parameter 0 != 0
            if parameters[0] != 0:
                i = parameters[1]
            else:
                i = i + 3
        elif opcode == 6: # jump if parameter 0 == 0
            if parameters[0] == 0:
                i = parameters[1]
            else:
                i = i + 3
        elif opcode == 7: # if parameter 0 < parameter 1, return address at 1, otherwise 0
            if parameters[0] < parameters[1]:
                store_at_address(st, mem, base + get_from_address(st, mem, i + 3), 1)
            else:
                store_at_address(st, mem, base + get_from_address(st, mem, i + 3), 0)
            i = i + 4
        elif opcode == 8: # parameter 0 == parameter 1, return address at 1, otherwise 0
            if parameters[0] == parameters[1]:
                store_at_address(st, mem, base + get_from_address(st, mem, i + 3), 1)
            else:
                store_at_address(st, mem, base + get_from_address(st, mem, i + 3), 0)
            i = i + 4
        elif opcode == 9: # change relative address to relative address + parameter 
            relative_address = relative_address + parameters[0]
            i = i + 2
        elif opcode == 99: # Halt
            print("Halted")
            return (0, -1, 0)

states = iP.dump_list_comma("day15")
states = [int(x) for x in states]

memory = [0]
position = (0,0)
zonemap = [(0,0,EMPTY)]
visited = [(0,0)]
manual = False

status, index, rel_addr = calculate(states, memory, NORTH)
if status != WALL:
    position = (0,1)
    zonemap.append((0,1,status))
else:
    zonemap.append((0,1,WALL))
print_map(zonemap, position)
while True:
    direction = -1
    add_x = 0
    add_y = 0
    
    if manual:
        di = input("Direction? (n/s/w/e/auto): ")
        if di == "n":
            direction = NORTH
            add_x = 0
            add_y = 1
        elif di == "s":
            direction = SOUTH
            add_x = 0
            add_y = -1       
        elif di == "w":
            direction = WEST
            add_x = -1
            add_y = 0
        elif di == "e":
            direction = EAST
            add_x = +1
            add_y = 0 
        if di == "auto":
            manual = False
            direction = NORTH
            add_x = 0
            add_y = 1
    else:  
        # Take preference first for unvisited areas:
        while True:
            if (position[0], position[1] + 1) in visited and (position[0], position[1] - 1) in visited and (position[0] - 1, position[1]) in visited and (position[0] + 1, position[1]) in visited:
                break
            direction = random.randrange(NORTH, EAST + 1)
            if direction == NORTH:
                add_x = 0
                add_y = 1
            elif direction == SOUTH:
                add_x = 0
                add_y = -1
            elif direction == WEST:
                add_x = -1 
                add_y = 0  
            elif direction == EAST:
                add_x = 1
                add_y = 0
            if (position[0] + add_x, position[1] + add_y) not in visited:
                break
        
        # If all zones are visited, pick random direction and, if no wall, go to it
        if direction == -1:
            #visited = [(position[0], position[1])] #Reset visited to avoid infinite loop
            while True:
                direction = random.randrange(NORTH, EAST + 1)
                if direction == NORTH:
                    add_x = 0
                    add_y = 1
                elif direction == SOUTH:
                    add_x = 0
                    add_y = -1
                elif direction == WEST:
                    add_x = -1 
                    add_y = 0  
                elif direction == EAST:
                    add_x = 1
                    add_y = 0

                if (position[0] + add_x, position[1] + add_y, WALL) not in zonemap: # No wall
                    break
    
    status, index, rel_addr = calculate(states, memory, direction)
    if (position[0] + add_x, position[1] + add_y,status) not in zonemap:
        zonemap.append((position[0] + add_x, position[1] + add_y,status))
    if (position[0] + add_x, position[1] + add_y) not in visited:
        visited.append((position[0] + add_x, position[1] + add_y))
    if status != WALL:
        position = (position[0] + add_x, position[1] + add_y)
    if status == OX_SYS or (position[0] == 0 and position[1] == 0):
        print("Found oxygen system or returned to origin!")
        if input("Take manual control (y/n)?") == "y":
            manual = True
    #think_about_walls(zonemap)
    print_map(zonemap, position)
    #input("")