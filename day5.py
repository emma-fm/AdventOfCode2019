import inputProcessor as iP

# st is an INTEGER list!
def calculate(st):
    i = 0
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
            value = int(input("Input: "))
            parameters = [value]
        elif opcode == 4:
            # Special case. Set mode to address (just in case)
            parameters = [0]
            mode[0] = 0

        # Calculate parameters for all opcodes but 3 and 99
        if opcode != 3 and opcode != 99:
            for j in range(0,len(parameters)):
                if mode[j] == 0: # position mode
                    parameters[j] = st[st[i + j + 1]]
                else: # immediate mode
                    parameters[j] = st[i + j + 1]

        # Operate
        if opcode == 1: # add parameters 0 and 1 and store them at direction pointed by 2
            st[st[i + 3]] = parameters[0] + parameters[1]
            i = i + 4
        elif opcode == 2: # multiply parameters 0 and 2 and store them at direction pointed by 2
            st[st[i + 3]] = parameters[0] * parameters[1]
            i = i + 4
        elif opcode == 3: # Store input at address of parameter 1
            st[st[i + 1]] = parameters[0]
            i = i + 2
        elif opcode == 4: # Return value at address at parameter 0
            print("Returned value ", parameters[0], " by instruction ", i)
            i = i + 2
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
                st[st[i + 3]] = 1
            else:
                st[st[i + 3]] = 0
            i = i + 4
        elif opcode == 8: # parameter 0 == parameter 1, return address at 1, otherwise 0
            if parameters[0] == parameters[1]:
                st[st[i + 3]] = 1
            else:
                st[st[i + 3]] = 0
            i = i + 4
        elif opcode == 99: # Halt
            print("Halted")
            return

states = iP.dump_list_comma("day5")
states = [int(x) for x in states]

calculate(states)