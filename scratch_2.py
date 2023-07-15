import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
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


radius = 5
seeds = generate_points(20, radius, "circle")

vor = Voronoi(seeds, incremental=True)
voronoi_plot_2d(vor, ax=ax, line_colors="blue", line_width=1, point_colors="gray")

areas = calculate_voronoi_cell_areas(vor)

# plot area in correct location
for i, ind in enumerate(vor.point_region):  # follows order of regions, then plots index
    plt.text(vor.points[i][0], vor.points[i][1] + 0.2, f'{areas[ind]:.3g}', ha='center', va='center')

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
