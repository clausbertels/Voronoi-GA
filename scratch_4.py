def calculate_voronoi_cell_areas(vor):
    areas = []
    for region in vor.regions:
        if -1 in region:
            areas.append(0)
        else:
            polygon = [vor.vertices[i] for i in region]
            areas.append(abs(area_signed(polygon)))
    return areas


def find_intersect(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return (x,y)


def calculate_voronoi_cell_areas(vor):
    areas = []
    for pt, region in enumerate(vor.regions):
        if -1 in region:
            open_region = region.remove(-1)
            polygon = [vor.vertices[i] for i in open_region]
            `for each ridge of region
                if it has two vertices (discounting -1):
                    find_intersect(v1, v2)
                if it has 1 vertex:
                    find its 2 points (aka seeds)
                    store average of those points in v1
                    store known vertex of ridge in v2
                    find_intersect(v1, v2)

            polygon.append(find_intersect())  # add the intersections
            areas.append(abs(area_signed(polygon)))
        else:
            polygon = [vor.vertices[i] for i in region]
            areas.append(abs(area_signed(polygon)))
    return areas





######

If -1 in region
    polygon = [vor.vertices[i] for i in region]
    polygon.append(intersections of ridges and circle)
    calculate polygon
    add segement area calculation (radius, two intersections)

if vertex out of bounds
