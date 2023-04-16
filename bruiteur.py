from random import randint
from math import *
import numpy as np
from PIL import Image

def dist_speciale(p1, p2, dim):
    i = p1[0] // (dim[0] // 2)
    j = p1[1] // (dim[1] // 2)
    i = 2 * i - 1
    j = 2 * j - 1
    dmin = inf
    for k in range(0, 2 * i, i):
        for l in range(0, 2 * j, j):
            dist = ((p1[0] - p2[0] - k * dim[0]) ** 2 + (p1[1] - p2[1] - l * dim[1]) ** 2)
            if dmin > dist:
                dmin = dist
    
    return dmin

def make_rand_grid(dim, nb_sommets):
    grid = np.ndarray(dim, float)
    for i in range(dim[0]):
        for j in range(dim[1]):
            grid[i, j] = 0
    
    pile = []
    for i in range(nb_sommets):
        x = randint(0, dim[0] - 1)
        y = randint(0, dim[1] - 1)

        pile.append((x, y))
        grid[x, y] = 0
    
    for i in range(dim[0]):
        if i % 10 == 0:
            print(i)
        for j in range(dim[1]):
            if not((i, j) in pile):
                mini = inf
                for e in pile:
                    distance = dist_speciale((i, j), e, dim)
                    if distance < mini:
                        mini = distance
                grid[i, j] = mini
    
    megamini = grid.max()
    for i in range(dim[0]):
        for j in range(dim[1]):
            grid[i, j] /= megamini
            grid[i, j] = sqrt(grid[i, j])

    return grid

def img_grid(grid, nom = "default.png"):
    dim = grid.shape
    img = Image.new("RGB", dim, (0, 0, 0))
    pix = img.load()

    for i in range(dim[0]):
        for j in range(dim[1]):
            pix[i, j] = int(255 * grid[i, j])
    
    img.save(nom)

img_grid(make_rand_grid((1000, 1000), 100))