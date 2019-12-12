import inputProcessor as iP

def calculate(st):
    for i in range(0, len(st), 4):
        if st[i] == 1:
            st[st[i + 3]] = st[st[i + 1]] + st[st[i + 2]]
        elif st[i] == 2:
            st[st[i + 3]] = st[st[i + 1]] * st[st[i + 2]]
        elif st[i] == 99:
            #print("Halted at position ", i)
            return st[0]
        else:
            #print("Unknown opcode at position ", i)
            return -1
            

states = iP.dump_list_comma("day2")
states = [int(i) for i in states]

# We need to copy because if we assigned it would copy the reference
original_states = states.copy()

# Replacements
states[1] = 12
states[2] = 2

print("Index 0 is: ", calculate(states))

output = 0
pairs = [(i,j) for i in range(0,100) for j in range(0,100)]

for p in pairs:
    states = original_states.copy()
    states[1] = p[0]
    states[2] = p[1]
    output = calculate(states)

    if output == 19690720:
        value = 100 * p[0] + p[1]
        print("Part 2 puzzle input is ", value)
        quit()