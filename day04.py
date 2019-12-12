import re

puzzle_input = range(265275,781585) # +1 to include last value

# If the input had values with less than 6 digits, you would have to add 0s to the left of them

# Two adjacent numbers are the same is:
# ^(?=.*(.)\1)[0-9]+$
# Digits never decrease is:
# ^0*1*2*3*4*5*6*7*8*9*$

fst= r"^(?=.*(.)\1)[0-9]+$"
snd = r"^0*1*2*3*4*5*6*7*8*9*$"

passwords = [x for x in puzzle_input if re.match(fst,str(x)) and re.match(snd, str(x))]

print("The quantity of passwords is: ", len(passwords))

# Now we check all the previous passwords to find which ones are valid under the new condition

true_passwords = []

for p in passwords:
    char = str(p)[0]
    quantity = 1
    good = False
    for i in range(1, len(str(p))):
        if char == str(p)[i]:
            quantity = quantity + 1
        elif char != str(p)[i] and quantity == 2:
            good = True
            break
        else:
            char = str(p)[i]
            quantity = 1
    if good or quantity == 2: # Needed in case there's two adjacent digits at the end
        true_passwords.append(p)

print("The new quantity of passwords is: ", len(true_passwords))