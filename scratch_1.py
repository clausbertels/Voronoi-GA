import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np

def plot_voronoi(size_x,size_y,vor,seed_text):
    fig = plt.figure(figsize=(8, 8), facecolor="lightgray")  # Adjust the figure size as needed
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_facecolor("white")
    voronoi_plot_2d(vor, ax=ax, line_colors="blue", line_width=1, point_colors="gray")
    plt.xlim(-(size_x+2), (size_x+2))
    plt.ylim(-(size_y+2), (size_y+2))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title("Voronoi Diagram")
    plt.grid(True)
    plt.gca().set_aspect('equal')

    # Display the area sizes as text
    for i, point in enumerate(vor.points):
        region_index = vor.point_region[i]
        if region_index in valid_regions:
            polygon = [vor.vertices[j] for j in vor.regions[region_index]]
            x, y = point
            area = areas[region_index]
            ax.text(x, y+0.2, f"{area:.2f}", ha='center', va='center', color='black')
    plt.show()


def generate_points(n, radius, shape_toggle="circle"):
    points = []
    while len(points) < n:
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        if (x * x + y * y) <= radius * radius or shape_toggle == "square":  # Check if point is within the circle, if not then it skips it
            points.append((x, y))

    return points


def calculate_areas(vor):
    for region_index in valid_regions:
        region = vor.regions[region_index]
        if -1 in region:
            areas[region_index] = 0  # sets the area to 0 if region contains an index -1, meaning infinite region
        else:
            polygon = [vor.vertices[i] for i in region]  # retrieves the verts of the current region
            area = 0.5 * abs(
                sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in zip(polygon, polygon[1:] + [polygon[0]])))
            areas[region_index] = area  # above line calculates area using shoelace algo


radius = 10
vor = Voronoi(generate_points(100, radius, "circle"))
areas = {}
valid_regions = set(filter(lambda x: x != -1 and len(vor.regions[x]) > 0, vor.point_region))

calculate_areas(vor)

plot_voronoi(10,10,vor,seed_text=0)



# pseudocode:
#     plot diagram function
#         in: view size, voronoi object, seed text (area size),
#            seed text == array with texts per seed object ordered by seed ID
#         process: generates a graphical matplotlib window
#         out: nothing
#
#     generate points function:
#         in: amount of points, radius
#         process: calculate random distribution of points as (x,y) positions
#         out: array of coordinates
#
#     calculate area function:
#         in: seed ID or seed coordinates?
#         process: calculate area size
#         out: area size for specific seed
#
#     call generate points
#
#     call calculate areas? Or maybe call the calculate area function inside the plot function higher up?
#
#     call plot