import inputProcessor as iP
import math

def group(need):
    new_need = []
    for i in range(0, len(need)):
        match = False
        for j in range(0, len(need)):
            if i != j and need[i][1] == need[j][1] and (need[i][0] + need[j][0], need[i][1]) not in new_need:
                new_need.append((need[i][0] + need[j][0], need[i][1]))
                match = True
                break
            elif (need[i][0] + need[j][0], need[i][1]) in new_need:
                match = True
                break
        if not match:
            new_need.append((need[i][0], need[i][1]))
    return new_need
    
reactions = iP.dump_list_newline("day14")
reactions = [r.split("=>") for r in reactions]
reactions = reactions[0:len(reactions) - 1] #Remove /n

tmp_results = [r[1][1:] for r in reactions] #Remove white space at the beginning


results = []
for r in tmp_results:
    tup = (int(r.split(" ")[0]), r.split(" ")[1])
    results.append(tup)

ingredients = [r[0].split(",") for r in reactions]
#Remove white spaces
new_ing = []
for i in ingredients:
    nt = []
    for t in i:
        elem = ""
        if t[0] == " " and t[-1] == " ":
            elem = t[1:len(t) - 1]
        elif t[0] == " ":
            elem = t[1:]
        elif t[-1] == " ":
            elem = t[0:len(t) - 1]
        else:
            elem = t
        nt.append(elem)
    new_ing.append(nt)

ingredients = []
for n in new_ing:
    l = []
    for e in n:
        tup = (int(e.split(" ")[0]), e.split(" ")[1])
        l.append(tup)
    ingredients.append(l)


need = [(1, "FUEL")]
waste = []
d = 0
while True:
    if len(need) == 1 and need[0][1] == "ORE":
        break
    element = need[d][1]
    quantity = need[d][0]
    for i in range(0, len(results)):
        if results[i][1] == element:
            times = 1
            if results[i][0] < quantity: # do we need to react more than once?
                times = math.ceil(quantity / results[i][0])
            need.remove((quantity, element))
            for j in ingredients[i]:
                match = False
                for w in waste:
                    if j[1] == w[1]:
                        if j[0] * times > w[0]:
                            need.append((j[0] * times - w[0], j[1]))
                            waste.remove(w)
                        elif j[0] * times < w[0]:
                            waste.remove(w)
                            waste.append((w[0] - j[0] * times, w[1]))
                        else:
                            waste.remove(w)
                        match = True
                        break
                if not match:
                    need.append((j[0] * times, j[1]))
            if results[i][0] * times - quantity > 0:
                waste.append(((results[i][0] * times) - quantity, element))
            d = d - 1
            break
    d = d + 1
    need = group(need)
    waste = group(waste)

print("Ore needed is: ", need[0][0])

maxfuel = 2
prevmaxfuel = 1
while True:
    need = [(maxfuel, "FUEL")]
    waste = []
    d = 0
    while True:
        if len(need) == 1 and need[0][1] == "ORE":
            break
        element = need[d][1]
        quantity = need[d][0]
        for i in range(0, len(results)):
            if results[i][1] == element:
                times = 1
                if results[i][0] < quantity: # do we need to react more than once?
                    times = math.ceil(quantity / results[i][0])
                need.remove((quantity, element))
                for j in ingredients[i]:
                    match = False
                    for w in waste:
                        if j[1] == w[1]:
                            if j[0] * times > w[0]:
                                need.append((j[0] * times - w[0], j[1]))
                                waste.remove(w)
                            elif j[0] * times < w[0]:
                                waste.remove(w)
                                waste.append((w[0] - j[0] * times, w[1]))
                            else:
                                waste.remove(w)
                            match = True
                            break
                    if not match:
                        need.append((j[0] * times, j[1]))
                if results[i][0] * times - quantity > 0:
                    waste.append(((results[i][0] * times) - quantity, element))
                d = d - 1
                break
        d = d + 1
        need = group(need)
        waste = group(waste)

    if need[0][0] < 1000000000000:
        prevmaxfuel = maxfuel
        maxfuel = maxfuel + 1
        print("try: ", maxfuel)
    else:
        break

print("Max fuel: ", maxfuel)