import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from skspatial.measurement import area_signed
from functions.func import generate_points, calc_area, find_connected_vertices, ridges_of_region, find_ridges_containing_index, is_ridge_intersecting_circle

# INITIATE PLOT
# Adjust the figure size as needed
fig = plt.figure(figsize=(8, 8), facecolor="lightgray")
ax = fig.add_subplot(111, aspect='equal')
ax.set_facecolor("white")

radius = 1
# seeds = [(0.1, 0.2), (0.1, 1.23), (0.05, 2.33), (1.23, 0.14), (1.25, 1.16),
#         (1.28, 2.8), (2.21, 0.42), (2.41, 1.54), (2.21, 2.26)]  # 9 seed points
seeds = [[0, 0], [-1, -1], [1, 1], [0, 1], [0, -1], [1, -1],
         [-1, 1], [1, 0], [-1, 0]]  # grid point pattern
seeds = generate_points(10, radius, "circle", False)

seeds.extend([(-2*radius, -2*radius), (-2*radius, 2*radius),
              (2*radius, -2*radius), (2*radius, 2*radius)])


vor = Voronoi(seeds, incremental=True)

# remove all empty arrays(in our case only one)
# vor.regions.remove([])

# reorder vor.regions by vor.point_region indices
vor.regions = [vor.regions[i] for i in vor.point_region]

# print("vor.vertices before plotting the area", vor.vertices)
# plot area index in correct location

for i, region in enumerate(vor.regions):
    plt.text(vor.points[i][0], vor.points[i][1] + 0.2,
             f'{calc_area(vor,i, radius):.5g}', ha='center', va='center')

# Plot vertex ID's in simple order of vor.vertices
for i, vertex in enumerate(vor.vertices):
    # why does it output "array([x,y])" when printed?
    plt.text(vertex[0], vertex[1] + 0.3, i, ha='center', va='center')

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

# print regions containing -1 (should always be exactly 4 because of corner points)
# for region in vor.regions:
    # if -1 in region:
    # print("regions containing -1: \n", region)

# print("points_with_id: \n", points_with_id)
# print("vor.point_region: \n", vor.point_region)
#print("vor.regions (reordered): \n", vor.regions)
#print("vor.vertices: \n", vor.vertices)
# print("vor.points (=seeds): \n", vor.points, "\n")

# print("vor.ridge_points: \n", vor.ridge_points)
#print("vor.ridge_vertices: \n", vor.ridge_vertices, "\n")

# print connected vertices to each vertex
# for i in range(len(vor.vertices)):
#    ridges = find_connected_vertices(vor, i)
#    print("ridges containing index: \n", ridges, "\n")

# print how many ridges intersect circle
# is_intersecting = []
# for i in range(len(vor.ridge_vertices)):
#    is_intersecting.append(is_ridge_intersecting_circle(radius, vor, i))
# print(is_intersecting.count(True))

# print ridges of each region
# for i in range(len(vor.regions)):
#    ridges_in_region = (ridges_of_region(vor, i))
#    print("Ridges in region:", ridges_in_region)

#Print total area
total_area = 0
for reg in range(len(vor.regions)):
    total_area += calc_area(vor, reg, radius)
print("Total area:", total_area)

# PLOT
voronoi_plot_2d(vor, ax=ax, line_colors="blue",
                line_width=1, point_colors="gray")
plt.xlim(-(radius + 2), (radius + 2))
plt.ylim(-(radius + 2), (radius + 2))
plt.xlabel('X')
plt.ylabel('Y')
plt.title("Voronoi Diagram")
plt.grid(True)
plt.gca().set_aspect('equal')

ax.add_patch(plt.Circle((0, 0), radius=radius, fill=False, color='gray'))

plt.show()

# NOTES
# vor.regions is in the order of vor.point_region's indexes
# vor.vertices is already ordered by their index, ascending
# vor.ridge_points is in the order of vor.points
# vor.ridge_vertices is in the order of vor.vertices
