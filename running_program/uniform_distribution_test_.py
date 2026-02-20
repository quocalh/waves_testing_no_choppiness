# generate a bunch of number
# get that qualitative data set, send to Desmos
# Desmos histogram

import random

n = 1000

print(random.random())

string = "l = ["

for i in range(n):
    string +=  f"{random.random()}, "

string = string[:-2]
string += "]"

print(string)

# all right, relatively good (up to around 70% to 80%)