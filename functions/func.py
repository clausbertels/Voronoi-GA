import random
import math
from scipy.spatial import Voronoi, voronoi_plot_2d, ConvexHull
import matplotlib.pyplot as plt
import numpy as np


def generate_points(n, circle_r, shape_toggle="circle"):
    points = []
    while len(points) < n:
        x = random.uniform(-circle_r, circle_r)
        y = random.uniform(-circle_r, circle_r)
        # Check if point is within the circle, if not then it skips it
        if (x**2 + y**2) <= circle_r**2 or shape_toggle == "square":
            points.append((x, y))
    circle_r *= 2
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


def calc_area(voronoi_object, index, radius):
    # this function calculates area of region for only selected index

    reg = voronoi_object.regions[index]
    #print(voronoi_object.points[index])
    vertices = voronoi_object.vertices

    # if the region is unbounded, return area of 0
    if -1 in reg:
        return 0

    else:
        outside_vertices = [vertex for vertex in reg if vertices[vertex][0]**2 + vertices[vertex][1]**2 > radius**2]
        intersection_points = []
        segment_area = 0
        if outside_vertices:
            region_ridges = ridges_of_region(voronoi_object, index)

            for ridge in region_ridges:
                point1 = vertices[ridge[0]]
                point2 = vertices[ridge[1]]
                intersection_points.append(
                    circle_line_segment_intersection(radius, point1, point2))

            # remove vertices outside of circle from region
            reg = [vertex for vertex in reg if vertex not in outside_vertices]

            # remove empty arrays in intersection points (apparently not needed)
            # intersection_points = [x for x in intersection_points if any(x)]

            # remove double brackets in intersection point array (didn't write this, it's so weird, but it works)
            intersection_points = [item for sublist in intersection_points for item in (
                sublist if isinstance(sublist, list) else [sublist])]

            # calculate circle segment area
            segment_area = circle_segment_area(
                intersection_points[0], intersection_points[1], radius)
            # print("Segment area:", segment_area)

        # create polygon from region vertices
        polygon = [vertices[i] for i in reg]
        #print(polygon)
        #print(intersection_points)

        # add intersection points to polygon
        ####### ISSUE: https://numpy.org/doc/stable/reference/generated/numpy.append.html
        ####### there's a problem with the formatting of all the differnt types of arrays, lists, tuples and what not. Needs to be unified.
        if intersection_points and polygon:
            polygon = np.append(polygon, intersection_points, axis=0)
        else:    
            polygon = intersection_points


        
        # calculate polygon area and add the segment area
        if len(polygon) > 2:
            polygon_area = ConvexHull(polygon).volume
            #print("polygon_area", polygon_area)
            return polygon_area + segment_area
        else:
            return segment_area


def find_ridges_containing_index(voronoi_object, index):
    # find all ridges that contain the given index
    ridges_indices = []
    for i,ridge in enumerate(voronoi_object.ridge_vertices):
        if np.isin(index, ridge).any():
            ridges_indices.append(i)
    return ridges_indices


def ridges_of_region(voronoi_object, index):
    region = voronoi_object.regions[index]
    ridges = []
    if -1 in region:
        return []
    for ridge in voronoi_object.ridge_vertices:
        if all(vertex in region for vertex in ridge):
            ridges.append(ridge)
    return ridges


def find_connected_vertices(voronoi_object, index):
    # find all ridges that contain the given index
    ridges_indices = find_ridges_containing_index(voronoi_object, index)
    ridges = [voronoi_object.ridge_vertices[i] for i in ridges_indices]

    # loop through the ridges and append the vertices that are not equal to the input index
    connected_vertices = []
    for ridge in ridges:
        for vertex in ridge:
            if vertex != index:
                connected_vertices.append(vertex)

    return connected_vertices

# this function wasn't made by me, I have no idea how but it works
def circle_line_segment_intersection(radius, p1, p2):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    dr = math.sqrt(dx**2 + dy**2)
    D = p1[0]*p2[1] - p2[0]*p1[1]
    discriminant = radius**2 * dr**2 - D**2

    if discriminant < 0:
        return []
    else:
        sign = 1 if dy >= 0 else -1
        x1 = (D*dy + sign * dx * math.sqrt(discriminant)) / dr**2
        y1 = (-D*dx + abs(dy) * math.sqrt(discriminant)) / dr**2
        x2 = (D*dy - sign * dx * math.sqrt(discriminant)) / dr**2
        y2 = (-D*dx - abs(dy) * math.sqrt(discriminant)) / dr**2

        # check if the intersection points are within the bounds of the line segment
        if (min(p1[0], p2[0]) <= x1 <= max(p1[0], p2[0])) and (min(p1[1], p2[1]) <= y1 <= max(p1[1], p2[1])):
            intersection1 = [x1, y1]
        else:
            intersection1 = None

        if (min(p1[0], p2[0]) <= x2 <= max(p1[0], p2[0])) and (min(p1[1], p2[1]) <= y2 <= max(p1[1], p2[1])):
            intersection2 = [x2, y2]
        else:
            intersection2 = None

        # return a list containing only the valid intersection points
        return [i for i in [intersection1, intersection2] if i is not None]


def circle_segment_area(p1, p2, radius):
    chord_length = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    theta = math.acos((radius**2 + radius**2 - chord_length**2)/(2*radius**2))
    area = 1/2 * (theta - math.sin(theta)) * radius**2
    return area


def shoelace_algo(polygon):
    n = len(polygon)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += polygon[i][0] * polygon[j][1] - polygon[j][0] * polygon[i][1]
    return area / 2.0

def map_to_01(array):
    sum_array = sum(array)
    for i,n in enumerate(array):
        array[i] = n / sum_array
    return array

def mapper(number,total):
    return number/total


def fitness(points, input_areas, radius):
    # print(len(points))
    # print(len(input_areas))
    circle_area = np.pi*(radius**2)
    sum_areas = 0
    points_copy = points.copy()
    points_copy.extend([(-2*radius, -2*radius), (-2*radius, 2*radius),
            (2*radius, -2*radius), (2*radius, 2*radius)])
    voronoi_object = Voronoi(points_copy)
    
    for i in range(len(points)):  # calculate area for every seed
        sum_areas += abs(mapper(calc_area(voronoi_object, i, radius), circle_area)
                          - mapper(input_areas[i], sum(input_areas)))
          # sum the differences (using abs to calculate the magnitude of deltas
    return abs(1 / sum_areas)  # this is the fitness score


def generate_random_unit_vector(dimensions):
    components = [np.random.normal() for i in range(dimensions)]
    r = math.sqrt(sum(x*x for x in components))
    vector = [x/r for x in components]
    return vector

