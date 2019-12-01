import inputProcessor as iP

mass_list = iP.dump_list("day1")
mass_list = [int(i) for i in mass_list]
totalfuel = 0
for m in mass_list:
    totalfuel = totalfuel + (int(m/3) - 2)

print("Total fuel requirement is: ", totalfuel)

totalfuel = 0

for m in mass_list:
    # The same as before but with an extra variable
    newfuel = int(m/3) - 2
    totalfuel = totalfuel + newfuel

    extrafuel = int(newfuel/3) - 2
    while extrafuel > 0:
        totalfuel = totalfuel + extrafuel
        extrafuel = int(extrafuel/3) - 2

print("The true fuel requirement is: ", totalfuel)