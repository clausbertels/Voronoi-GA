import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
from functions.func import generate_points, display_points


points = generate_points(25, 10)
# display_points(points, 10)

voronoi_plot_2d(Voronoi(points))
plt.show()
