import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import ConvexHull
import numpy as np
from skspatial.measurement import area_signed

seeds = [(0, 0), (0, 2), (0, 4), (2, 0), (2, 2), (2, 4), (4, 0), (4, 2), (4, 4)]  # 9 seed points


def generate_points(n, radius, shape_toggle = 0):
    points = []
    while len(points) < n:
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        if (x*x + y*y) <= radius*radius or shape_toggle == 1:  # Check if point is within the circle, if not then it skips it
            points.append((x, y))

    return points

def generate_custom_grid(x_resolution, y_resolution, grid_size):
    points = []
    for i in range(x_resolution):
        for j in range(y_resolution):
            x = i * grid_size / (x_resolution - 1)
            y = j * grid_size / (y_resolution - 1)
            points.append([x, y])
    return np.array(points)
#seeds = generate_points(10, 1, 1)
seeds = generate_custom_grid(10,10,10)

vor = Voronoi(seeds, incremental=True)

voronoi_plot_2d(vor)

def calculate_voronoi_cell_areas(vor):
    areas = []
    for region in vor.regions:
        if -1 in region:
            areas.append(0)
        else:
            polygon = [vor.vertices[i] for i in region]
            areas.append(abs(area_signed(polygon)))
   
    return areas
def calculate_voronoi_region_areas_2(vor):

area = calculate_voronoi_cell_areas(vor)
print("area calc: \n", area)

# plot seed ID according to point_region ID
for i, seed in enumerate(seeds):
    plt.text(seed[0], seed[1]+0.05, "{:.2f}".format(area[i]), ha='center', va='center')

# just for double checking, array not really needed, I think
#points_with_id = [] 
#for i, seed in enumerate(seeds):
#    points_with_id.append([vor.point_region[i], seed])

#print("points_with_id: \n", points_with_id)
print("vor.point_region: \n", vor.point_region)
print("vor.regions: \n", vor.regions)
print("vor.vertices: \n", vor.vertices)
print("vor.points: \n", vor.points, "\n")

# add ID's to list of vertices
vertices_with_id = []
for i, vertex in enumerate(vor.vertices):
    vertices_with_id.append([i, vor.vertices[i]])

print("vertices_with_id: \n", vertices_with_id)


bounded_regions = []
for arr in vor.regions:
    if arr and not any(num == -1 for num in arr):
        bounded_regions.append(arr)

print("bounded_regions: \n", bounded_regions)

plt.show()


