import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np


def generate_points(n, radius):
    points = []
    while len(points) < n:
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        if (x ** 2 + y ** 2) <= radius * radius:  # Check if point is within the circle, if not then it skips it
            points.append((x, y))

    return points


def display_points(points, radius):
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]

    plt.scatter(x_values, y_values)
    plt.xlim(-(radius + 1), (radius + 1))  # the +1 is just to zoom out a bit more than the radius of the circle
    plt.ylim(-(radius + 1), (radius + 1))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'{len(points)} Points in Circle of Radius {radius}')
    plt.grid(True)
    plt.gca().set_aspect('equal')
    plt.show()
    voronoi_plot_2d(points)

points = generate_points(25, 10)
#display_points(points, 10)

voronoi_plot_2d(Voronoi(points))
plt.show()