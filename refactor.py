import matplotlib.pyplot as plt
from random import random
from scipy.spatial import Voronoi, voronoi_plot_2d
from itertools import pairwise
from math import dist, acos, sin, cos, pi, atan2
from operator import itemgetter
from functools import cmp_to_key


def length(p: tuple[float, float]) -> float:
    """Length of a point from (0, 0). Same as math.dist((0, 0), pt)"""
    return sum(i ** 2 for i in p) ** 0.5


def randcolor() -> tuple[float, float, float]:
    """Random color, tuple of 3 floats."""
    return random(), random(), random()


def draw_point(pt: tuple[float, float], color=None):
    """Draw a point on the plot."""
    plt.plot(*pt, marker="o", markersize=6, markerfacecolor=color or "black", markeredgewidth=1, markeredgecolor="black")


def draw_dashed_line(p1, p2=(0, 0), color="black"):
    plt.plot(*((p2[0], p1[0]), (p2[1], p1[1])), color=color, linewidth=1, dashes=(2, 2), linestyle='dashed')


def draw_poly(poly, ax):
    from matplotlib.patches import Polygon
    polygon1 = Polygon(poly)
    polygon1.set_color(randcolor())
    ax.add_patch(polygon1)


def draw_line(p1, p2=(0, 0), color="red"):
    plt.plot(*((p2[0], p1[0]), (p2[1], p1[1])), color=color)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


# Element wise add then multiply by factor
def addmul_f(p1, p2, f):
    return p1[0] + p2[0] * f, p1[1] + p2[1] * f


def line_point_fac(p, l1, l2):
    u = l2[0] - l1[0], l2[1] - l1[1]
    d = u[0] * u[0] + u[1] * u[1]
    if d > 0.0:
        return dot(u, (p[0] - l1[0], p[1] - l1[1])) / d
    return 0.0


# Line-sphere intersection
def isect_line_sphere(line: tuple[float, float], r: float) -> list[tuple[float, float]]:
    """Return a list of intersection points between a line and a circle."""

    (x1, y1), (x2, y2) = (l1, l2) = line
    ldir = x2 - x1, y2 - y1  # line direction
    a = dot(ldir, ldir)
    b = 2.0 * (ldir[0] * x1 + ldir[1] * y1)
    i = b * b - 4.0 * a * (dot(l1, l1) - (r * r))

    if i >= 0:
        if i == 0.0:
            ret = [addmul_f(l1, ldir, -b / (2.0 * a))]
        else:
            i_sqrt = i ** 0.5
            a2 = 1 / (2.0 * a)
            ret = [addmul_f(l1, ldir, (-b + i_sqrt) * a2),
                   addmul_f(l1, ldir, (-b - i_sqrt) * a2)]

        return [i for i in ret if 0.0 <= line_point_fac(i, l1, l2) <= 1.0]
    return []


def calc_segment_area(chord: tuple[float, float], radius: float) -> float:
    """Calculate the area of a segment given a chord and the circle's radius."""
    theta = acos((radius ** 2 + radius ** 2 - dist(*chord) ** 2) / (2 * radius ** 2))
    return (theta - sin(theta)) * radius ** 2 * 0.5


def calc_segment_area_ex(chord: tuple[float, float], radius: int | float, is_major=False):
    """Calculate the segment area based on a chord and a circle's radius.
    optional parameter 'is_major' returns the inverse area.
    """
    ret = calc_segment_area(chord, radius)
    if is_major:
        ret = (pi * radius ** 2) - ret
    return ret


def calc_poly_area(coords: list[tuple[float, float]]) -> float:
    """Calculate the area of a convex polygon. The coordinates must be ordered and
    the sequence must have a length of 3 (triangle) or more."""
    n2 = 0
    x2, y2 = coords[-1]
    for co in coords:
        x, y = co
        n2 += (x + x2) * (y2 - y)
        x2 = x
        y2 = y
    return abs(n2 * 0.5)


# Same as calc_poly_area, but for triangles. Can be substituted.
def calc_tri_area(v1, v2, v3):
    return abs(0.5 * ((v1[0] - v2[0]) * (v2[1] - v3[1]) + (v1[1] - v2[1]) * (v3[0] - v2[0])))


chords = []
polygons = []


# Convenience function
def draw(vor, radius):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig = voronoi_plot_2d(vor, ax)

    # Set plot bounds
    pad = 0.5
    plt.xlim(-radius - pad, radius + pad)
    plt.ylim(-radius - pad, radius + pad)
    draw_point((0, 0))

    for line in chords:
        draw_line(*line)

    for poly in polygons:
        draw_poly(poly, ax)

    # Draw circle boundary
    circle = plt.Circle((0, 0), radius)
    circle.set_color((0, 1, 0, 0.0))
    circle.set_edgecolor((0, 0, 0, 1))
    ax.set_aspect(1)
    ax.add_artist(circle)
    plt.show()


def make_seed_chords_for_circle(points: int, radius: int | float):
    co = []
    while True:
        r, theta = [(random() ** 0.5) * radius, 2 * pi * random()]
        x = round(r * cos(theta), 3)
        y = round(r * sin(theta), 3)
        if length((x, y)) < radius:
            co.append((x, y))
            if len(co) >= points:
                break
    assert all(length(c) <= radius for c in co), \
        f"Some of the seed coordinates are outside the circle: {co}"

    bvd = radius * 10
    return co + [(-bvd, -bvd), (bvd, -bvd), (bvd, bvd), (-bvd, bvd)]


def get_intersections(vor: Voronoi, radius: int) -> dict:
    """Takes a voronoi object and circle radius yields a tuple of polygon
    and intersection points. Only polygons that intersect with the circle's
    boundary is returned.
    """
    data = []
    vertices = vor.vertices
    for r in vor.regions:
        if -1 not in r and r:
            p = itemgetter(*r)(vertices)

            isects = []      # Intersection points
            for line_index, line in enumerate(pairwise(p[-1:] + p)):
                if ret := isect_line_sphere(line, radius):
                    isects.append((ret, line_index))
            data.append((p, isects))
    return data


def verts_in_circle(poly, radius):
    """Given a poly and radius, return a set of vertices of the poly whose
    points are within the circle's radius.
    """
    verts = set()
    for point in poly:
        if length(point) <= radius:
            verts.add(tuple(point))
    return verts


def calc_poly_center(p):
    """Calculate the unweighted center of a polygon."""
    assert len(p) > 2
    x1 = y1 = 1e10
    x2 = y2 = -x1
    for i in range(-2, len(p) - 2, 2):
        for j in range(3):
            x, y = p[i + j]
            x1 = min(x, x1)
            x2 = max(x, x2)
            y1 = min(y, y1)
            y2 = max(y, y2)
    return (x1 + x2) * 0.5, (y1 + y2) * 0.5


def center_of_points(a, b):
    """The center of two points"""
    return (a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5


def order_verts_cw(poly):
    """Takes a convex polygon and orders its vertices clockwise"""
    cx = cy = 0
    for px, py in poly:
        cx += px
        cy += py
    cx /= len(poly)
    cy /= len(poly)

    def sorter(a, b):
        a1 = atan2(a[0] - cx, a[1] - cy) + (2 * pi)
        a2 = atan2(b[0] - cx, b[1] - cy) + (2 * pi)
        return a1 - a2
    return sorted(poly, key=cmp_to_key(sorter))


def main(num_cells):
    chords.clear()
    polygons.clear()
    global vor, radius

    radius = 1.0
    area_circle = pi * radius ** 2
    # cells = [25, 47, 28] # input area sizes sum to 100 (percent) to be used in fitness function

    # num_cells = len(cells)
    # num_cells = 50

    seed_coords = make_seed_chords_for_circle(num_cells, radius)
    vor = Voronoi(seed_coords)

    n = 0           # Current cell being calculated
    record = []     # Info about the cell calculation, for inspection
    area_summed = 0
    cell_areas = [] # Store the calculated area per cell

    #   poly: The (whole) polygon that intersects with the circle
    # isects: The intersection points for lines
    for poly, isects_data in get_intersections(vor, radius):
        isects = [pt for isect, index in isects_data for pt in isect]
        num_isects = len(isects)

        # The cell is contained. We just calculate the poly area.
        if not num_isects:
            area = calc_poly_area(poly)
            polygons.append(poly)

        # The cell intersects with the circle.
        else:
            area = 0  # To be summed in the loop
            verts = verts_in_circle(poly, radius)

            # Cell is a segment.
            # Before writing it off as a segment, check if the intersecting lines'
            # points are outside of the circle. If not, then include the triangle.
            if num_isects == 2:
                i1, i2 = isects
                is_major = False

                # Center of intersections i1 i2
                ic = center_of_points(i1, i2)

                # Try to determine if the segment is major by
                # 1. Construct line between ic and polygon center (pc)
                # 2. Find circle boundary intersection i3  (isect_line_sphere)
                # 3. Compare the distance between i3 and radius.
                pc = calc_poly_center(poly)
                for i3 in isect_line_sphere((ic, pc), radius):
                    if dist(i3, ic) > radius:
                        is_major = True

                if verts:
                    inner_poly = order_verts_cw(verts | {i1, i2})
                    area += calc_poly_area(inner_poly)
                    polygons.append(inner_poly)
                try:
                    area += calc_segment_area_ex(isects, radius, is_major)
                # May fail on exactly 50-50 two segment split.
                except ValueError:
                    area += area_circle * 0.5

                chords.append(isects)

            # Cell has two ridges that intersect with the circle boundary.
            elif num_isects == 4:
                isects_set = set(isects)

                # Cell has two chords. Procedure for finding them is:
                # 1. Order the verts that form the cell (clock-wise)
                # 2. Loop over the verts and form a possible chord
                # 3. Check that the chord points don't belong to   the same line.
                cell = order_verts_cw(verts | set(isects))
                polygons.append(cell)
                for p1, p2 in pairwise(cell[-1:] + cell):
                    if p1 in isects_set and p2 in isects_set:
                        p1_line = p2_line = -1
                        for isect, index in isects_data:
                            if p1 in isect and p1_line == -1:
                                p1_line = index
                            if p2 in isect and p2_line == -1:
                                p2_line = index
                        # p1 and p2 are on distinct lines. They form a chord.
                        if p1_line != p2_line:
                            chords.append((p1, p2))  # For visual
                            area += calc_segment_area((p1, p2), radius)  # First segment

                poly = order_verts_cw(verts | set(isects))
                polygons.append(poly)  # For visual
                area += calc_poly_area(poly)

        cell_areas.append(area)
        area_summed += area
        n += 1

    deviance = area_circle - area_summed

    # Bad. Cell area calculations are off.
    if abs(deviance) > 0.0001:
        print(f"Bad result: ({abs(deviance)} deviance) chords:{len(chords)}\n")
        for string in record:
            print(string)

        draw(vor, radius)
        raise Exception  # End the loop

    # Good. Cell areas sum up to circle area.
    else:
        if not do_draw:
            return

        r_percentage = 100 / area_circle
        cell_area_percentages = [a * r_percentage for a in cell_areas]

        string = ", ".join(f"{ap:.1f}" for ap in cell_area_percentages)
        # print(f"Good result! Cell area percentages: {string}")
        # draw(vor, radius)

vor = None
radius = None

if __name__ == "__main__":

    do_draw = True
    n = 0
    from random import randint
    while True:
        print(n, end="\r")
        main(randint(2, 30))
        n += 1
