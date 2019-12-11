import inputProcessor as iP
import math

puzzle = "test"

asteroids = iP.dump(puzzle)
width = len((iP.dump_list_newline(puzzle))[0])
height = len(iP.dump_list_newline(puzzle))
asteroids = [x for x in asteroids if x != "\n"]

ast = []
for i in range(0,len(asteroids)):
    if asteroids[i] == "#":
        x = i % width
        y = math.ceil(i / width) - 1 # 0 indexing
        ast.append((x,y))

asteroids = ast

viewedBy = []
for a in asteroids:
    tmp = asteroids.copy()
    count = 0
    for b in asteroids:
        if b in tmp and b is not a:
            count = count + 1
            for c in asteroids:
                if c is not a and c is not b:
                    # Is c in the line between a and b?
                    # (y - y1) == (y2 - y1)/(x2 - x1) * (x - x1)
                    try:
                        if c[1] - a[1] == (b[1] - a[1])/(b[0] - a[0]) * (c[0] - a[0]):
                            tmp.remove(c)
                    except ZeroDivisionError as ex: # For division by 0
                        pass

    viewedBy.append(count)

print("Max detected asteroids: ", max(viewedBy))