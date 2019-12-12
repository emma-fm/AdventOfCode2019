import inputProcessor as iP
import numpy as np
from PIL import Image

width = 25
height = 6

picture = iP.dump("day8")
picture = picture[0:len(picture)] # Remove \n

layers = []
number_of_layers = int(len(picture) / (width * height))

index = 0
for i in range(0,number_of_layers): #layer
    layers.append("")
    for j in range(0,width*height): #we only have to count pixels, so no need for 2D array
        layers[i] = layers[i] + picture[index]
        index = index + 1

max_quantity = [99999999,0,0] #Quantity of 0, 1 and 2
for l in layers:
    if l.count('0') < max_quantity[0]:
        max_quantity[0] = l.count('0')
        max_quantity[1] = l.count('1')
        max_quantity[2] = l.count('2')


print("Number of 1 * Number of 2: ", max_quantity[1] * max_quantity[2])

result = ""
for i in range(0, width * height):
    for l in layers:
        if l[i] != "2": # Not transparent
            result = result + l[i]
            break

pixels = [[(0,0,0) for j in range (0,width)] for i in range(0,height)]

index = 0
for i in range(0,len(pixels)):
    for j in range(0,len(pixels[i])):
        if (result[index] == "1"):
            pixels[i][j] = (255,255,255)
        index = index + 1

array = np.array(pixels, dtype=np.uint8)
image = Image.fromarray(array)
image.save("result.png")
print("Result saved to result.png")