import inputProcessor as iP

def repeat_pattern(pattern, times):
    val = []
    for i in range(0, len(pattern)):
        for j in range(0, times):
            val.append(pattern[i])
    return val

input_signal = iP.dump("day16")
input_signal = [int(x) for x in input_signal.replace("\n","")]

offset = input_signal.copy()
for i in range(0,100):
    new = []
    for j in range(0,len(offset)):
        p = 1 # Pattern index to apply
        pattern = repeat_pattern([0,1,0,-1], j + 1)
        tmp = []
        for o in offset:
            tmp.append(o * pattern[p])
            p = p + 1
            if p == len(pattern):
                p = 0
        value = abs(sum(tmp))
        if value % 10 != value:
            value = value % 10
        new.append(value)
    offset = new.copy()

print("First 8 values of result list: ", offset[0:8])

# PART 2 NOT DONE