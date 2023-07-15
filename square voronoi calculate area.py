import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import ConvexHull
import numpy as np
from skspatial.measurement import area_signed

###### INITIATE PLOT
fig = plt.figure(figsize=(8, 8), facecolor="lightgray")  # Adjust the figure size as needed
ax = fig.add_subplot(111, aspect='equal')
ax.set_facecolor("white")

def generate_points(n, radius, shape_toggle="circle"):
    points = []
    while len(points) < n:
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        if (
                x * x + y * y) <= radius * radius or shape_toggle == "square":  # Check if point is within the circle, if not then it skips it
            points.append((x, y))

    return points


def calculate_voronoi_cell_areas(vor):
    areas = []
    for region in vor.regions:  # follows order of regions array
        if -1 in region:
            areas.append(0)
        else:
            polygon = [vor.vertices[i] for i in region]
            areas.append(abs(area_signed(polygon)))
    return areas


# seeds = [(0.1, 0.2), (0.1, 1.23), (0.05, 2.33), (1.23, 0.14), (1.25, 1.16), (1.28, 2.8), (2.21, 0.42), (2.41, 1.54), (2.21, 2.26)]  # 9 seed points
radius = 5
seeds = generate_points(7, radius, "circle")

vor = Voronoi(seeds, incremental=True)
voronoi_plot_2d(vor, ax=ax, line_colors="blue", line_width=1, point_colors="gray")

areas = calculate_voronoi_cell_areas(vor)

# plot area index in correct location
for i, ind in enumerate(vor.point_region):  # follows order of regions, then plots index
    plt.text(vor.points[i][0], vor.points[i][1] + 0.2, f'{i:.3g}', ha='center', va='center')

# Plot vertex ID's in simple order of vor.vertices
for i, vertex in enumerate(vor.vertices):
    plt.text(vertex[0], vertex[1] + 0.3, i, ha='center', va='center')  # why does it output "array([x,y])" when printed?

# plot seed ID according to point_region ID
# for i, seed in enumerate(seeds):  # follows order of seeds array, then plots correct index number on seed location
#    plt.text(seed[0], seed[1] + 0.05, vor.point_region[i], ha='center', va='center')

# inverted from above, should give same result
# for i, ind in enumerate(vor.point_region):  # follows order of regions, then plots index
#    plt.text(vor.points[i][0], vor.points[i][1] + 0.05, f'{areas[ind]:.3g}', ha='center', va='center')

# just for double-checking, array not really needed, I think
# points_with_id = []
# for i, seed in enumerate(seeds):
#    points_with_id.append([vor.point_region[i], seed])

# print("points_with_id: \n", points_with_id)
print("vor.point_region: \n", vor.point_region)
print("vor.regions: \n", vor.regions)
print("vor.vertices: \n", vor.vertices)
print("vor.points (=seeds): \n", vor.points, "\n")

print("vor.ridge_points: \n", vor.ridge_points)
print("vor.ridge_vertices: \n", vor.ridge_vertices, "\n")

bounded_regions = []
for arr in vor.regions:
    if arr and not any(num == -1 for num in arr):
        bounded_regions.append(arr)

print("bounded_regions: \n", bounded_regions)

###### PLOT

plt.xlim(-(radius+2), (radius+2))
plt.ylim(-(radius+2), (radius+2))
plt.xlabel('X')
plt.ylabel('Y')
plt.title("Voronoi Diagram")
plt.grid(True)
plt.gca().set_aspect('equal')

plt.show()

###### NOTES
# vor.regions is in the order of vor.point_region's indexes
# vor.vertices is already ordered by their index, ascending
# vor.ridge_points is in the order of vor.points
# vor.ridge_vertices is in the order of vor.vertices