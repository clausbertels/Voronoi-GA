import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from functions.func import (calc_area, generate_points, fitness)

radius = 10
# input_areas = [2,3,5,2,3,1,4,7,2,3,6,9,2,3,1] # 15 areas
input_areas = np.random.randint(0,10,15).tolist()
areas_length = len(input_areas)
generations = 100
treshold = 999
iterations = 10

prevGen = []
for _ in range(iterations):  # generate 100 random lists of length n with each tuple set within circle bounds
    points = generate_points(areas_length, radius, "circle")
    points.extend([(-2*radius, -2*radius), (-2*radius, 2*radius),
              (2*radius, -2*radius), (2*radius, 2*radius)])
    prevGen.append(points)
    points = [] 


for g in range(generations):  # ######## GENERATION LOOP ##########
    ranked = []
    for solution in prevGen:  # list every solution with its fitness score
        vor = Voronoi(solution)
        ranked.append((fitness(solution, input_areas, vor, radius), solution))
    ranked.sort()
    ranked.reverse()

    print("top score: ", ranked[0][0])
    if ranked[0][0] > treshold:  # stop "evolving" when good enough fitness score threshold is
        print("Approximate solution found")
        break

    best = ranked[:10]  # grab top ten best solutions

    best_ordered = []
    for i in range(areas_length):
        best_ordered.append([])
        for e in best: 
            best_ordered[i].append(e[1][i])

    newGen = []
    for _ in range(iterations):  # generate a hundred solutions based on the previous hundred random solutions
        for c in range(areas_length):
            x = random.choice(best_ordered[c])[0] * random.uniform(0.99, 1.01)
            y = random.choice(best_ordered[c])[1] * random.uniform(0.99, 1.01)
            points.append((x, y))
        newGen.append(points)
        points = []

    prevGen = newGen
