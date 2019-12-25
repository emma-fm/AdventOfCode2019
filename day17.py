import inputProcessor as iP

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
def calculate(st, mem, i=0, relative_address=0, inpt=[]):
    while i < len(st):
        inp_index = 0
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
            value = inpt[inp_index]
            inp_index = inp_index + 1
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
            return(0,-1,0)

states = iP.dump_list_comma("day17")
states = [int(x) for x in states]
og_states = states.copy()

memory = [0]
value, index, rel_addr = calculate(states, memory)
scaffold = []
x = 0
y = 0
while index != -1:
    if value == 35 or value == 118 or value == 60 or value == 62 or value == 94:
        scaffold.append((x,y))

    x = x + 1

    if value == 10: #line break
        y = y + 1
        x = 0
    value, index, rel_addr = calculate(states, memory, index, rel_addr)

intersection = []
for s in scaffold:
    if (s[0] + 1, s[1]) in scaffold and (s[0] - 1, s[1]) in scaffold and (s[0], s[1] + 1) in scaffold and (s[0], s[1] - 1) in scaffold:
        intersection.append(s)

### Print with marked intersections ###
memory = [0]
states = og_states.copy()
value, index, rel_addr = calculate(states, memory)
x = 0
y = 0
while index != -1:
    if value == 10: #line break
        y = y + 1
        x = 0

    if (x,y) in intersection:
        print("O", end="")
    else:
        print(chr(value), end="")
    value, index, rel_addr = calculate(states, memory, index, rel_addr)
    x = x + 1
#########

distances = 0
for i in intersection:
    distances = distances + (i[0] * i[1])

print("Sum of the alignment parameters: ", distances)

memory = [0]
states = og_states.copy()
states[0] = 2

'''
    10 left
    4 up
    2 left
    10 up
    6 left
    6 down
    12 right
    2 down
    2 left
    6 down
    2 right
    4 up
    3 left
    3 right
    2 up
    8 right
    6 up
    12 left
    8 down
    8 right
    8 down
    4 right
    2 down
    6 right
    12 up
    6 right
    10 up
    12 right
    12 down
    10 left
    10 down
    12 right
    6 down
    6 up
    12 left
    10 up
10 right
12 up
12 left
10 down
6 left
12 down
10 left
2 up
6 left
4 up
2 right
2 down
10 left
10 down
10 left
6 down
6 right
6 up
4 right
6 up
6 right
10 down
12 right
10 up

10,L,4,U,2,L,10,U,6,L,6,D,12,R,2,D,2,L,6,D,2,R,4,U,3,L,3,R,2,U,8,R,6,U,12,L,8,D,8,R,8,D,4,R,2,D,6,R,12,U,6,R,10,U,12,R,12,D,10,L,10,D,12,R,6,D,6,U,12,L,10,U,10,R,12,U,12,L,10,D,6,L,4,U,2,R,2,D,10,L,10,D,10,L,6,D,6,R,6,U,4,R,6,U,6,R,10,D,12,R,10,U
'''