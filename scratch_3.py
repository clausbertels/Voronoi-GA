import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from functions.func import (calc_area, generate_points, fitness)

# INITIATE PLOT
# Adjust the figure size as needed
fig = plt.figure(figsize=(8, 8), facecolor="gray")
ax = fig.add_subplot(111, aspect='equal')
ax.set_facecolor("white")


# INITIAL PARAMETERS
radius = 10
input_areas = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#points = [(0.15, 0.2), (0.1, 1.23), (0.05, 2.33), (1.23, 0.14), (1.25, 1.16),(1.28, 2.8), (2.21, 0.42), (2.41, 1.54), (2.21, 2.26)]  # 9 seed points
#points = [[0, 0], [-1, -1], [1, 1], [0, 1], [0, -1], [1, -1], [-1, 1], [1, 0], [-1, 0]]  # grid point pattern
points = [(0.9140222415785377, -2.278077309428255), (0.4095026738049796, 6.2666640979905495), (-2.1350035670974554, 9.597577370077747), (-1.4580563528339354, 3.4168290377158677), (-7.061562030124833, 1.774371232509239), (-1.1499240443849974, 6.425810957156635), (5.467506779670735, -2.3759464758858435), (-8.461836441702618, 1.8530766624259716), (3.47736409405454, 6.008007878023189)]
#points = [(1.637673132787734, 3.4081119817128567), (1.4446965527704254, 0.7979874758661882), (6.428378401923496, 4.2262953105361145), (1.5966708340949776, 0.5912057965229938), (1.821550200149007, -8.025261992111792), (2.0488680720974806, 9.271960084864343), (2.2621869501189558, 6.536988546120185), (-2.504576164481529, -3.12683617525866), (0.15758059899696875, -4.162303016294533)]
#points = [(6.68952222305062, 1.6074241453323417), (0.9736775449885542, -3.9758260957263314), (5.682607656607397, -2.8305635004186662), (2.0449606109262817, -6.09069323689627), (4.604179596185482, -7.272246042647432), (5.200863442274937, -2.807508974426394), (4.537613395665774, 1.7643094147927734), (-2.0493372059557835, -0.815014793203801), (-3.1362509777615326, -9.241912307166103), (-2.2011314546658216, 9.52029105133176), (1.1478090431540302, 5.6182670275267395), (7.693873028867944, -5.153121031907957), (-9.791215731487187, -1.59392468749453), (1.1338699971456663, 7.6814776261454085), (-7.163333163643426, -1.3827459895144898), (4.143813479545866, -7.30697672412054), (-1.4046389038756253, -7.668722974156415), (-2.3208253923263396, 3.3185249198093647), (6.039938899625845, 2.1518087128337076)]


#points = generate_points(100, radius, "circle")

#print(points)

# Add 4 corner points
points.extend([(-2*radius, -2*radius), (-2*radius, 2*radius),
            (2*radius, -2*radius), (2*radius, 2*radius)])

# Create Voronoi Diagram
vor = Voronoi(points)

# reorder vor.regions by vor.point_region indices
vor.regions = [vor.regions[i] for i in vor.point_region]


# plot area in correct location and calculate total area

total_area = 0
for i, region in enumerate(vor.regions):
    cell_area = 0
    cell_area = calc_area(vor,i,radius)
    
    plt.text(vor.points[i][0], vor.points[i][1] + 0.2,
            f'{i:.3g}', ha='center', va='center')
    total_area += cell_area

print("Total area:", total_area)



# Plot vertex ID's in simple order of vor.vertices
for i, vertex in enumerate(vor.vertices):
    # why does it output "array([x,y])" when printed?
    plt.text(vertex[0], vertex[1] + 0.2, i, ha='center', va='center')

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
# print("vor.regions (reordered): \n", vor.regions)
# print("vor.vertices: \n", vor.vertices)
# print("vor.points (=seeds): \n", vor.points, "\n")

# print("vor.ridge_points: \n", vor.ridge_points)
# print("vor.ridge_vertices: \n", vor.ridge_vertices, "\n")

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




# PLOT
voronoi_plot_2d(vor, ax=ax, line_colors="blue",
                line_width=1, point_colors="gray")
plt.xlim(-(radius + 2), (radius + 2))
plt.ylim(-(radius + 2), (radius + 2))
plt.xlabel('X')
plt.ylabel('Y')
plt.title("Voronoi Diagram, Total Area of cells: " + str(total_area))
plt.grid(True)
plt.gca().set_aspect('equal')

ax.add_patch(plt.Circle((0, 0), radius=radius, fill=False, color='gray'))

plt.show()

# NOTES
# vor.regions is in the order of vor.point_region's indexes
# vor.vertices is already ordered by their index, ascending
# vor.ridge_points is in the order of vor.points
# vor.ridge_vertices is in the order of vor.vertices
