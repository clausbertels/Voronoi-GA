import random
from skspatial.measurement import area_signed
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt


def generate_points(n, circle_r, shape_toggle="circle", corner_toggle=False):
    points = []
    while len(points) < n:
        x = random.uniform(-circle_r, circle_r)
        y = random.uniform(-circle_r, circle_r)
        # Check if point is within the circle, if not then it skips it
        if (x * x + y * y) <= circle_r * circle_r or shape_toggle == "square":
            points.append((x, y))
    # below code is for adding corner points
    circle_r *= 2
    if corner_toggle:
        points.extend([(-circle_r, -circle_r), (-circle_r, circle_r),
                       (circle_r, circle_r), (circle_r, -circle_r)])
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

# this one is here just in case but it's very messy and not very useful, the plot can be made with a few lines of code anyways
def display_points(points, radius):
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]

    plt.scatter(x_values, y_values)
    # the +1 is just to zoom out a bit more than the radius of the circle
    plt.xlim(-(radius + 1), (radius + 1))
    plt.ylim(-(radius + 1), (radius + 1))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'{len(points)} Points in Circle of Radius {radius}')
    plt.grid(True)
    plt.gca().set_aspect('equal')
    plt.show()
    voronoi_plot_2d(points)

# this one calculates area of region for only selected index, which probably makes more sense than the other function
def calc_area(voronoi_object, index):
    reg = voronoi_object.regions[index]
    if -1 in reg:
        return 0
    else:
        polygon = [voronoi_object.vertices[i] for i in reg]
        return abs(area_signed(polygon))
