import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import Delaunay
import numpy as np
from scipy.spatial import ConvexHull

def generate_points(n, radius, shape_toggle = 0):
    points = []
    while len(points) < n:
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        if (x*x + y*y) <= radius*radius or shape_toggle == 1:  # Check if point is within the circle, if not then it skips it
            points.append((x, y))

    return points

def display_points(points, radius):
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]
    
    plt.scatter(x_values, y_values)
    plt.xlim(-(radius+2), (radius+2)) #the +1 is just to zoom out a bit more than the radius of the circle
    plt.ylim(-(radius+2), (radius+2))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'{len(points)} Points in Circle of Radius {radius}')
    plt.grid(True)
    plt.gca().set_aspect('equal')
    plt.show()
    
#generate the points
points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                   [2, 0], [2, 1], [2, 2]]) #grid point pattern
points = generate_points(100, 10, 1)
def generate_custom_grid(x_resolution, y_resolution, grid_size):
    points = []
    for i in range(x_resolution):
        for j in range(y_resolution):
            x = i * grid_size / (x_resolution - 1)
            y = j * grid_size / (y_resolution - 1)
            points.append([x, y])
    return np.array(points)
#points = generate_custom_grid(3,3,8)


vor = Voronoi(points)



# Calculate the cell areas
areas = {}
valid_regions = set(filter(lambda x: x != -1 and len(vor.regions[x]) > 0, vor.point_region))
for region_index in valid_regions:
    region = vor.regions[region_index]
    if -1 in region:
        areas[region_index] = 0 # sets the area to 0 if region contains an index -1, meaning infinite region
    else:
        polygon = [vor.vertices[i] for i in region] #retrieves the verts of the current region
        area = 0.5 * abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in zip(polygon, polygon[1:] + [polygon[0]])))
        areas[region_index] = area #above line calculates area using shoelace algo


# Plot the Voronoi diagram
fig = plt.figure(figsize=(8, 8), facecolor ="gray")  # Adjust the figure size as needed
ax = fig.add_subplot(111, aspect='equal')
ax.set_facecolor("black")
voronoi_plot_2d(vor, ax=ax, line_colors = "blue", line_width = 2, point_colors = "blue")
plt.xlim(-(10), (10))
plt.ylim(-(10), (10))
plt.xlabel('X')
plt.ylabel('Y')
plt.title("Voronoi Diagram")
plt.grid(True)
plt.gca().set_aspect('equal')

# Display the areas as text
for i, point in enumerate(vor.points):
    region_index = vor.point_region[i]
    if region_index in valid_regions:
        polygon = [vor.vertices[j] for j in vor.regions[region_index]]
        x, y = point
        area = areas[region_index]
        ax.text(x, y, f"{area:.2f}", ha='center', va='center', color='orange') #the .2f is the decimal precision, only for the displaying text tho, calculated area stays the same
plt.show()




#display_points(points, 10)
#print(vor.vertices) #vertex positions of vertices created by the voronoi diagram for example:
#[[0.5 0.5] [0.5 1.5] [1.5 0.5] [1.5 1.5]]
#print(vor.regions) #vertex id's of each region, for example [0,1,3,2] which is a square (also can output -1
# which means that point is just at infinity)
#print(vor.points) #all the point positions you input for the voronoi function, so from vor = Voronoi(points) it is the "points"
#print(vor.point_region) #all region id's: [1 3 2 8 7 9 6 4 5]
#print(vor.max_bound)
#print(vor.min_bound)
#print(vor.ndim)
#print(vor.npoints)

#print(areas)


