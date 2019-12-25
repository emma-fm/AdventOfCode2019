import inputProcessor as iP

NUMBER_OF_CARDS = 10007

def stack(deck):
    list.reverse(deck)

def cut(quant,deck):
    if quant > 0:
        unit = deck[:quant]
        deck = deck[quant:]
        for u in unit:
            deck.append(u)
        return deck
    else:
        unit = deck[quant:]
        deck = deck[:len(deck) + quant]
        for d in deck:
            unit.append(d)
        return unit

def increment(quant,deck):
    old_deck = deck.copy()
    i = 0 # Index to insert
    j = 0 # Index to get
    shuffled = 0 # Quantity of shuffled cards
    while shuffled < NUMBER_OF_CARDS:
        deck[i] = old_deck[j]
        j = j + 1
        i = i + quant
        if i > NUMBER_OF_CARDS - 1:
            i = i - NUMBER_OF_CARDS
        shuffled = shuffled + 1

actions = iP.dump_list_newline("day22")
actions = actions[:len(actions) - 1] # Remove last line

formatted_actions = []
for a in actions:
    if "cut" in a:
        quant = int(a[4:])
        formatted_actions.append(("cut",quant))
    elif "increment" in a:
        quant = int(a[20:])
        formatted_actions.append(("increment",quant))
    elif "stack" in a:
        formatted_actions.append(("stack",0)) # Number is arbitrary

actions = formatted_actions

deck = [x for x in range(0,NUMBER_OF_CARDS)]

for a in actions:
    if a[0] == "stack":
        stack(deck)
    elif a[0] == "cut":
        deck = cut(a[1],deck)
    elif a[0] == "increment":
        increment(a[1],deck)

print("Position of card 2019: ", deck.index(2019))