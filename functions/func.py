import random
from skspatial.measurement import area_signed
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

def generate_points(n, radius, shape_toggle="circle"):
    points = []
    while len(points) < n:
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        if (x * x + y * y) <= radius * radius or shape_toggle == "square":  # Check if point is within the circle, if not then it skips it, or toggles the shape to square
            points.append((x, y))

    return points

def calculate_voronoi_cell_areas(voronoi):
    areas = []
    for region in voronoi.regions:  # follows order of regions array
        if -1 in region:
            areas.append(0)
        else:
            polygon = [voronoi.vertices[i] for i in region]
            areas.append(abs(area_signed(polygon)))
    return areas


#this one is here just in case but it's very messy and not very useful, the plot can be made with a few lines of code anyways
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

