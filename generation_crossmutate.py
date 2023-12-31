import random
import numpy as np
from functions.func import (generate_points, fitness, generate_random_unit_vector)

RADIUS = 10
# input_areas = [2,3,5,2,3,1,4,7,2,3,6,9,2,3,1] # 15 areas
AREAS_LENGTH = 15
input_areas = np.random.randint(0,10,AREAS_LENGTH).tolist()
GENERATIONS = 500
TRESHOLD = 999
DEVIATION = 0.01
ITERATIONS = 500
BEST_AMOUNT = 5

prevGen = []
for _ in range(ITERATIONS):  # generate x random lists of length n with each tuple set within circle bounds
    points = generate_points(AREAS_LENGTH, RADIUS, "circle")
    prevGen.append(points)
    #print(prevGen)
    #print(points)
    #print(fitness(points, input_areas, RADIUS)) # big waste of resources to print this

points = [] # flush points array



for g in range(GENERATIONS):  ######## GENERATION LOOP ##########
    ranked = []
    for solution in prevGen:  # list every solution with its fitness score, [solution] == [points]
        fitness_score = fitness(solution, input_areas, RADIUS)
        ranked.append((fitness_score, solution))
    ranked.sort()
    ranked.reverse()

    print("top score: ", ranked[0][0])

    if ranked[0][0] > TRESHOLD:  # stop "evolving" when good enough fitness score threshold is
        print("Approximate solution found")
        break

    best = ranked[:BEST_AMOUNT]  # grab top x best solutions
    # TODO: trim off the fitness scores from this list (best) so we don't have to use [1] in best_ordered

    best_ordered = [] 
    for r in range(AREAS_LENGTH):
        best_ordered.append([]) # generate a list for each region ordered by the region index
        for s in best: # for every solution in best
            best_ordered[r].append(s[1][r]) # grab a point by the region index and add it to its respective list
                                            # [1] skips the fitness score and [r] selects 

    newGen = []
    for _ in range(ITERATIONS):  # generate x solutions based on the previous hundred random solutions
        for r in range(AREAS_LENGTH): # for each region
            random_vector = generate_random_unit_vector(2)
            rand = random.choice(best_ordered[r]) # pick a random point (x,y)
            x = rand[0] + random_vector[0] * DEVIATION
            y = rand[1] + random_vector[1] * DEVIATION
            points.append((x, y))
        newGen.append(points)
        points = []

    prevGen = newGen
    
