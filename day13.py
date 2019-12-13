import inputProcessor as iP

def find_on_tiles(tile_num, tiles):
    for t in tiles:
        if tiles[t] == tile_num:
            return t

def print_board(tiles):
    max_y = max([t[1] for t in tiles])
    for file in range(0, max_y):
        for t in tiles:
            if t[1] == file:
                char = ""
                if tiles[t] == 0:
                    char = " "
                elif tiles[t] == 1:
                    char = "X"
                elif tiles[t] == 2:
                    char = "#"
                elif tiles[t] == 3:
                    char = "_"
                elif tiles[t] == 4:
                    char = "O"
                print(char, end="")
            elif t[1] < file:
                continue
            else:
                print("")
                break

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
def calculate(st, mem, relative_address=0, i=0, tiles={}, autoplay=False):
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
            if autoplay:
                if tiles != {}:
                    ball_x = find_on_tiles(4, tiles)[0]
                    paddle_x = find_on_tiles(3, tiles)[0]
                    if paddle_x < ball_x: #paddle left of ball
                        value = 1
                    elif paddle_x > ball_x: #paddle right of ball
                        value = -1
                    else:
                        value = 0
            else:
                value = input("Direction <- a d -> or wait(enter): ")
                if "a" in value:
                    value = -1
                elif "d" in value:
                    value = 1
                else:
                    value = 0
            parameters = [value,0]
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
            return (0,-1,0)

states = iP.dump_list_comma("day13")
states = [int(x) for x in states]

original_states = states.copy()

memory = [0]
tiles = []
blocks = 0

x, index, rtaddr = calculate(states, memory)
y, index, rtaddr = calculate(states, memory, rtaddr, index)
tile, index, rtaddr = calculate(states, memory, rtaddr, index)

while True:
    tiles.append((x,y,tile))
    if tile == 2: #block tile
        blocks = blocks + 1
    

    x, index, rtaddr = calculate(states, memory, rtaddr, index)
    if index == -1:
        break
    y, index, rtaddr = calculate(states, memory, rtaddr, index)
    tile, index, rtaddr = calculate(states, memory, rtaddr, index)

print("Number of blocks: ", blocks)


states = original_states
states[0] = 2
memory = []
tiles = {}
score = 0
auto = False


x, index, rtaddr = calculate(states, memory)
y, index, rtaddr = calculate(states, memory, rtaddr, index)
tile, index, rtaddr = calculate(states, memory, rtaddr, index)

inp = input("Autoplay? (y/n): ")
if inp == "y":
    auto = True

while True:
    tiles[(x,y)] = tile

    print("SCORE: ", score)
    if not auto:
        print_board(tiles)

    x, index, rtaddr = calculate(states, memory, rtaddr, index, tiles, auto)
    if index == -1:
        break
    y, index, rtaddr = calculate(states, memory, rtaddr, index, tiles, auto)
    tile, index, rtaddr = calculate(states, memory, rtaddr, index, tiles, auto)

    if x == -1 and y == 0 and tile > score:
        score = tile

print("Your score: ", score)