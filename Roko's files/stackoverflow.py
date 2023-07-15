import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.morphology import binary_erosion
from scipy.spatial import Voronoi
from shapely.geometry import Point, Polygon
from skimage import draw
from sklearn.neighbors import KDTree

def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.
    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()*2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)



def get_circular_se(radius=2):

    N = (radius * 2) + 1
    se = np.zeros(shape=[N,N])
    for i in range(N):
        for j in range(N):
                se[i,j] = (i - N / 2)**2 + (j - N / 2)**2 <= radius**2
    se = np.array(se, dtype="uint8")
    return se

def polygonize_by_nearest_neighbor(pp):
    """Takes a set of xy coordinates pp Numpy array(n,2) and reorders the array to make
    a polygon using a nearest neighbor approach.

    """

    # start with first index
    pp_new = np.zeros_like(pp)
    pp_new[0] = pp[0]
    p_current_idx = 0

    tree = KDTree(pp)

    for i in range(len(pp) - 1):

        nearest_dist, nearest_idx = tree.query([pp[p_current_idx]], k=4)  # k1 = identity
        nearest_idx = nearest_idx[0]

        # finds next nearest point along the contour and adds it
        for min_idx in nearest_idx[1:]:  # skip the first point (will be zero for same pixel)
            if not pp[min_idx].tolist() in pp_new.tolist():  # make sure it's not already in the list
                pp_new[i + 1] = pp[min_idx]
                p_current_idx = min_idx
                break

    pp_new[-1] = pp[0]
    return pp_new


#generates a circular mask
side_len = 256
rad = 100
mask = np.zeros(shape=(side_len, side_len))
rr, cc = draw.circle_perimeter(int(side_len/2), int(side_len/2), radius=int(rad), shape=mask.shape)

mask[rr, cc] = 1

#makes a polygon from the mask perimeter
se = get_circular_se(radius=1)
contour = mask - binary_erosion(mask, structure=se)
pixels_mask = np.array(np.where(contour==1)[::-1]).T
polygon = polygonize_by_nearest_neighbor(pixels_mask)
polygon = Polygon(polygon)

#generates random seeds
points_x = np.random.random_integers(0,side_len,250)
points_y = np.random.random_integers(0,side_len,250)
points = (np.vstack((points_x,points_y))).T

# returns a list of the centroids that are contained within the polygon
new_points = []
for point in points:
    if polygon.contains(Point(point)):
        new_points.append(point)

#performs voronoi tesselation
if len(points) > 3: #otherwise the tesselation won't work
    vor = Voronoi(new_points)
    regions, vertices = voronoi_finite_polygons_2d(vor)

    #clips tesselation to the mask
    new_vertices = []
    for region in regions:
        poly_reg = vertices[region]
        shape = list(poly_reg.shape)
        shape[0] += 1
        p = Polygon(np.append(poly_reg, poly_reg[0]).reshape(*shape)).intersection(polygon)
        poly = (np.array(p.exterior.coords)).tolist()
        new_vertices.append(poly)

    #plots the results
    fig, ax = plt.subplots()
    ax.imshow(mask,cmap='Greys_r')
    for poly in new_vertices:
        ax.fill(*zip(*poly), alpha=0.7)
    ax.plot(points[:,0],points[:,1],'ro',ms=2)
    plt.show()

    