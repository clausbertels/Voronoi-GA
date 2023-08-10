import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from functions.func import (calc_area, generate_points, fitness, generate_random_unit_vector)

radius = 10
# input_areas = [2,3,5,2,3,1,4,7,2,3,6,9,2,3,1] # 15 areas
input_areas = np.random.randint(0,10,10).tolist()
areas_length = len(input_areas)
generations = 500
treshold = 999
deviation = 0.1
iterations = 500
best_amt = 5

prevGen = []
for _ in range(iterations):  # generate x random lists of length n with each tuple set within circle bounds
    points = generate_points(areas_length, radius, "circle")
    prevGen.append(points)
    #print(prevGen)
    #print(points)
    #print(fitness(points, input_areas, radius)) # big waste of resources to print this

points = [] # flush points array



for g in range(generations):  ######## GENERATION LOOP ##########
    ranked = []
    for solution in prevGen:  # list every solution with its fitness score, [solution] == [points]
        fitness_score = fitness(solution, input_areas, radius)
        ranked.append((fitness_score, solution))
    ranked.sort()
    ranked.reverse()

    print("top score: ", ranked[0][0])

    if ranked[0][0] > treshold:  # stop "evolving" when good enough fitness score threshold is
        print("Approximate solution found")
        break

    best = ranked[:best_amt]  # grab top x best solutions

    best_ordered = []
    for i in range(areas_length):
        best_ordered.append([])
        for e in best: 
            best_ordered[i].append(e[1][i])

    newGen = []
    for _ in range(iterations):  # generate x solutions based on the previous hundred random solutions
        for c in range(areas_length):
            random_vector = generate_random_unit_vector(2)
            rand = random.choice(best_ordered[c])
            x = rand[0] + random_vector[0] * deviation
            y = rand[1] + random_vector[1] * deviation
            points.append((x, y))
        newGen.append(points)
        points = []

    prevGen = newGen
    
