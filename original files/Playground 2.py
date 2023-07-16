import math
import random
from scipy.spatial import Voronoi as Vor

cells = [25, 47, 28]  # input area sizes sum to 100 (percent) to be used in fitness function
n = len(cells)

prevGen = []
co = []

for _ in range(10):  # generate 100 random lists of length n with each tuple set within circle bounds
    for _ in range(n):
        r, theta = [math.sqrt(random.random()) * 5, 2 * math.pi * random.random()]  # replace 5 with circle radius
        x = round(r * math.cos(theta), 1)
        y = round(r * math.sin(theta), 1)
        co.append((x, y))
    prevGen.append(co)
    co = []

def fitness(seeds):
    return random.random()*998


for g in range(100):  # ######## GENERATION LOOP ##########
    ranked = []
    for s in prevGen:  # list every solution with its fitness score
        ranked.append((fitness(s), s))
    ranked.sort()
    ranked.reverse()

    print(ranked[0])
    if ranked[0][0] > 999:  # stop "evolving" when good enough fitness score threshold is
        print("Approximate solution found")
        break

    best = ranked[:5]  # grab top ten best solutions

    best_ordered = []
    for i in range(n):  # list of three
        best_ordered.append([])
        for e in best:  # list of five
            best_ordered[i].append(e[1][i])