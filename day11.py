from enum import Enum
import inputProcessor as iP
from PIL import Image
import numpy as np


class Pointing(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

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
def calculate(st, mem, inpt, relative_address=0, i=0):
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
            return (-1,0,0)

states = iP.dump_list_comma("day11")
states = [int(x) for x in states]

original_states = states.copy()

memory = [0]

robotpos = (0,0)
looking_at = Pointing.UP
rel_addr = 0
index = 0
white = []
painted = []
color = 0
direction = 0
over_color = 0

while True:
    if robotpos in white:
        over_color = 1
    else:
        over_color = 0

    (color, index, rel_addr) = calculate(states,memory,over_color,relative_address=rel_addr,i=index)
    if color == -1:
        break
    (direction, index, rel_addr) = calculate(states,memory,over_color,relative_address=rel_addr,i=index)

    if color == 1:
        if robotpos not in painted:
            painted.append(robotpos)
        white.append(robotpos)
    if color == 0:
        if robotpos in white:
            white.remove(robotpos)
    
    if looking_at == Pointing.UP and direction == 0:
        looking_at = Pointing.LEFT
        robotpos = (robotpos[0] - 1, robotpos[1])
    elif looking_at == Pointing.UP and direction == 1:
        looking_at = Pointing.RIGHT
        robotpos = (robotpos[0] + 1, robotpos[1])
    elif looking_at == Pointing.DOWN and direction == 0:
        looking_at = Pointing.RIGHT
        robotpos = (robotpos[0] + 1, robotpos[1])
    elif looking_at == Pointing.DOWN and direction == 1:
        looking_at = Pointing.LEFT
        robotpos = (robotpos[0] - 1, robotpos[1])
    elif looking_at == Pointing.LEFT and direction == 0:
        looking_at = Pointing.DOWN
        robotpos = (robotpos[0], robotpos[1] - 1)
    elif looking_at == Pointing.LEFT and direction == 1:
        looking_at = Pointing.UP
        robotpos = (robotpos[0], robotpos[1] + 1)
    elif looking_at == Pointing.RIGHT and direction == 0:
        looking_at = Pointing.UP
        robotpos = (robotpos[0], robotpos[1] + 1)
    elif looking_at == Pointing.RIGHT and direction == 1:
        looking_at = Pointing.DOWN
        robotpos = (robotpos[0], robotpos[1] - 1)
    else:
        raise Exception("Direction error")

print("Painted tiles at least once: ", len(painted))


states = original_states
memory = [0]

robotpos = (0,0)
looking_at = Pointing.UP
rel_addr = 0
index = 0
white = [(0,0)]
painted = []
color = 0
direction = 0
over_color = 0

while True:
    if robotpos in white:
        over_color = 1
    else:
        over_color = 0

    (color, index, rel_addr) = calculate(states,memory,over_color,relative_address=rel_addr,i=index)
    if color == -1:
        break
    (direction, index, rel_addr) = calculate(states,memory,over_color,relative_address=rel_addr,i=index)

    if color == 1:
        if robotpos not in painted:
            painted.append(robotpos)
        white.append(robotpos)
    if color == 0:
        if robotpos in white:
            white.remove(robotpos)
    
    if looking_at == Pointing.UP and direction == 0:
        looking_at = Pointing.LEFT
        robotpos = (robotpos[0] - 1, robotpos[1])
    elif looking_at == Pointing.UP and direction == 1:
        looking_at = Pointing.RIGHT
        robotpos = (robotpos[0] + 1, robotpos[1])
    elif looking_at == Pointing.DOWN and direction == 0:
        looking_at = Pointing.RIGHT
        robotpos = (robotpos[0] + 1, robotpos[1])
    elif looking_at == Pointing.DOWN and direction == 1:
        looking_at = Pointing.LEFT
        robotpos = (robotpos[0] - 1, robotpos[1])
    elif looking_at == Pointing.LEFT and direction == 0:
        looking_at = Pointing.DOWN
        robotpos = (robotpos[0], robotpos[1] - 1)
    elif looking_at == Pointing.LEFT and direction == 1:
        looking_at = Pointing.UP
        robotpos = (robotpos[0], robotpos[1] + 1)
    elif looking_at == Pointing.RIGHT and direction == 0:
        looking_at = Pointing.UP
        robotpos = (robotpos[0], robotpos[1] + 1)
    elif looking_at == Pointing.RIGHT and direction == 1:
        looking_at = Pointing.DOWN
        robotpos = (robotpos[0], robotpos[1] - 1)
    else:
        raise Exception("Direction error")


x = [w[0] for w in white]
y = [w[1] for w in white]

offset_x = abs(min(0, min(x)))
offset_y = abs(min(0, min(y)))

white = [(a + offset_x, b + offset_y) for (a,b) in white]

x = [w[0] for w in white]
y = [w[1] for w in white]

width = max(x) + 1
height = max(y) + 1

pixels = [[(0,0,0) for j in range (0,height)] for i in range(0,width)]
for w in white:
    pixels[w[0]][w[1]] = (255,255,255)

array = np.array(pixels, dtype=np.uint8)
image = Image.fromarray(array)
image.save("result.png")
print("Result saved to result.png. May be flipped.")