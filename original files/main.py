import math
import random
from scipy.spatial import Voronoi as Vor

cells = [25, 47, 28, 16]  # input area sizes relative to each other
n = len(cells)

prevGen = []
co = []

for _ in range(100):  # generate 100 random lists of length n with each tuple set within circle bounds
    for _ in range(n):
        r, theta = [math.sqrt(random.random()) * 5, 2 * math.pi * random.random()]  # replace 5 with circle radius
        x = round(r * math.cos(theta), 1)
        y = round(r * math.sin(theta), 1)
        co.append((x, y))
    prevGen.append(co)
    co = []


def area(seed):  # takes the coords of the vertices
    coords = Vor(seed).vertices
    n2 = 0
    x2, y2 = coords[-1]
    for co in coords:  # Shoelace algorithm to calculate area of polygon
        x, y = co
        n2 += (x + x2) * (y2 - y)
        x2 = x
        y2 = y
    return abs(n2 * 0.5)  # area of chosen vertices


# def fitness_old(seeds):
#    sum_areas = 0
#    for i, seed in enumerate(seeds):  # calculate area for every seed
#        sum_areas += abs(area(seed) - cells[i])  # sum the differences (using abs to calculate the magnitude of deltas
#    return abs(1 / sum_areas)  # this is the fitness score

def fitness(seeds):
    areas_ordered = []
    for seed in seeds:  # 1. calculate area sizes of regions
        areas_ordered.append(area(seed))
    areas_ordered.sort()  # 2. rank area sizes of regions from small to big
    cells_ordered = cells.sort()  # 3. rank input cell sizes from small to big

    sum_areas = 0
    for i, a in enumerate(areas_ordered):  # 4. compare sizes and sum absolute deltas
        sum_areas += abs(a - cells_ordered[i])  # add each delta amount to total deviation
    return abs(1 / sum_areas)  # this is the fitness score per solution set


for g in range(1000):  # ######## GENERATION LOOP ##########
    ranked = []
    for solution in prevGen:  # list every solution with its fitness score
        ranked.append((fitness(solution), solution))
    ranked.sort()
    ranked.reverse()

    print(ranked[0])
    if ranked[0][0] > 999:  # stop "evolving" when good enough fitness score threshold is
        print("Approximate solution found")
        break

    best = ranked[:10]  # grab top ten best solutions

    best_ordered = []
    for i in range(n):  # list of three
        best_ordered.append([])
        for e in best:  # list of five
            best_ordered[i].append(e[1][i])

    newGen = []
    for _ in range(100):  # generate a hundred solutions based on the previous hundred random solutions
        for c in range(n):
            x = random.choice(best_ordered[c])[0] * random.uniform(0.99, 1.01)
            y = random.choice(best_ordered[c])[1] * random.uniform(0.99, 1.01)
            co.append((x, y))
        newGen.append(co)
        co = []

    prevGen = newGen
