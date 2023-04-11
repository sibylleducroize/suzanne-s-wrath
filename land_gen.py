from math import *
from random import uniform as unif
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

R2 = sqrt(2)

def t_cube(t):
    return t * (3 * t - 2 * t ** 2)

def rotation_matrix(theta):
    s = sin(theta)
    c = cos(theta)
    return np.array([[c, -s], [s, c]])

def t_cube2(point, square):
    p = point
    s = square
    r = s[0]
    r += (s[1] - s[0]) * t_cube(p[0])
    r += (s[3] - s[0]) * t_cube(p[1])
    r += (s[0] - s[1] + s[2] - s[3]) * t_cube(p[0]) * t_cube(p[1])
    return r

def make_random_grid(dim, inf, sup):
    grid = np.ndarray(dim, float)
    for i in range(dim[0]):
        for j in range(dim[1]):
            grid[i, j] = unif(inf, sup)
    
    return grid

def t_cube_interpol(grid, point):
    i = int(point[0])
    j = int(point[1])

    x = point[0] - i
    y = point[1] - j

    point1 = [x, y]
    square = [grid[i, j], grid[i + 1, j], grid[i + 1, j + 1], grid[i, j + 1]]

    return t_cube2(point1, square)

def perlin(grid, point, amplitudes, frequences, mat_rot = rotation_matrix(1), fmod = lambda i, j : j):
    levels = len(amplitudes)
    max_coord = min(grid.shape)
    p = point.copy()
    for i in range(2):
        p[i] -= .5
    assert(levels == len(frequences))
    assert(max(frequences) * R2 < max_coord)
    
    res = 0
    rot = np.array([[1, 0], [0, 1]])
    for i in range(levels):
        p_bis = []
        for j in range(2):
            p_bis.append((p[j] + .5 * R2) * frequences[i])
        
        res += amplitudes[i] * fmod(i, t_cube_interpol(grid, p_bis))
        p = p @ mat_rot
    
    return res / sum(amplitudes)
