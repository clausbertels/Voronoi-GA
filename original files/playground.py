from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import numpy as np
from math import dist, acos, sin, cos, pi
from random import random


def length(p: tuple[float, float]) -> float:
    """Length of a point from (0, 0). Same as math.dist((0, 0), pt)"""
    return sum(i ** 2 for i in p) ** 0.5


def make_seed_chords_for_circle(points: int, radius: int | float):
    co = []
    while True:
        r, theta = [(random() ** 0.5) * radius, 2 * pi * random()]
        x = round(r * cos(theta), 3)
        y = round(r * sin(theta), 3)
        if length((x, y)) < radius:
            co.append((x, y))
            if len(co) >= points:
                break
    assert all(length(c) <= radius for c in co), \
        f"Some of the seed coordinates are outside the circle: {co}"
    co.extend([(-2 * radius, -2 * radius), (2 * radius, -2 * radius), (2 * radius, 2 * radius), (-2 * radius, 2 * radius)])
    return co


seeds_coords = np.array(make_seed_chords_for_circle(10, 5))
vor = Voronoi(seeds_coords)

figure, axes = plt.subplots()
cc = plt.Circle((0, 0), 5, fc="green")

axes.set_aspect(1)
axes.add_artist(cc)

fig = voronoi_plot_2d(vor)
plt.show()

'''
def fitness(seeds):
    sum_areas = 0
    for i, seed in enumerate(seeds):  # calculate area for every seed
        sum_areas += abs(area(seed) - cells[i])  # sum the differences
    return abs(1 / sum_areas)  # this is the fitness score


for g in range(1000):  # ######## GENERATION LOOP ##########
    ranked = []
    for s in prevGen:  # list every solution with its fitness score
        ranked.append((fitness(s), s))
'''
