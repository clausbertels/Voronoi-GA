import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from functions.func import (generate_points, fitness, generate_random_unit_vector)

RADIUS = 10
# input_areas = [2,3,5,2,3,1,4,7,2,3,6,9,2,3,1] # 15 areas
AREAS_LENGTH = 15
input_areas = np.random.randint(0,10,AREAS_LENGTH).tolist()
GENERATIONS = 5000
THRESHOLD = 999
DEVIATION = 0.2
ITERATIONS = 600
BEST_AMOUNT = 1

prevGen = []
for _ in range(ITERATIONS):  # generate x random lists of length n with each tuple set within circle bounds
    points = generate_points(AREAS_LENGTH, RADIUS, "circle")
    prevGen.append(points)
    #print(prevGen)
    #print(points)
    #print(fitness(points, input_areas, RADIUS)) # big waste of resources to print this

points = [] # flush points array for use in newgen 

for g in range(GENERATIONS):  ######## GENERATION LOOP ##########
    ranked = []
    for solution in prevGen:  # list every solution with its fitness score, [solution] == [points]
        fitness_score = fitness(solution, input_areas, RADIUS)
        ranked.append((fitness_score, solution))
    ranked.sort(reverse=True)

    print("top score: ", ranked[0][0])

    if ranked[0][0] > THRESHOLD:  # stop "evolving" when good enough fitness score threshold is met
        print("Approximate solution found")
        break

    best = ranked[0][1]

    newGen = []
    for x in range(ITERATIONS): # do the below x amount of times to create a new generation of solutions
        for p in range(AREAS_LENGTH): # for every point in best[], deviate the x and y coords
            random_vector = generate_random_unit_vector(2)
            x = best[p][0] + random_vector[0] * DEVIATION
            y = best[p][1] + random_vector[1] * DEVIATION
            points.append((x, y))
        newGen.append(points)
        points = []

    prevGen = newGen
