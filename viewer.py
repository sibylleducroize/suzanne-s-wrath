#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured
from transform import normalized, normal_vec
from math import exp

from land_gen import make_random_grid, perlin, volcano


# -------------- Example textured plane class ---------------------------------
class TexturedPlane(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        # setup plane mesh to be textured
        base_coords = ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0))
        scaled = 100 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)


class HeightMap(Mesh):
    """ HeighMap, with z the vertical axis """

    """ Creates a grid whose x and y coordinates are contained within the render cube.
        The scaling applied is the same on both the x and y axis."""
    def __init__(self, shader, grid, **uniforms):
        # grid should be a numpy array
        dim = grid.shape
        dimax = max(dim) - 1
        ratio = 2 / dimax
        dim_total = dim[0] * dim[1]

        vertex_list = []
        for i in range(dim[0]):
            for j in range(dim[1]):
                x = i * ratio - 1
                y = j * ratio - 1
                z = grid[i, j]
                point = (x, y, z)
                vertex_list.append(point)
        
        position = np.array(vertex_list, np.float32)

        index_list = []
        for i in range(dim[0] - 1):
            for j in range(dim[1] - 1):
                orientation = (i + j) % 2
                dx = orientation
                dy = 0
                for k in range(5):
                    x = i + dx
                    y = j + dy
                    index_list.append(y + dim[1] * x)

                    # start of the second triangle and end of the first, this point is needed two times
                    if k == 2:
                        index_list.append(y + dim[1] * x)
                    dp = (k + orientation) % 2
                    dx = (dx + dp + 1) % 2
                    dy = (dy + dp) % 2

        index = np.array(index_list, np.uint32)
        
        normal = np.ndarray((dim_total, 3), np.float32)
        for i in range(dim_total):
            normal[i] = np.array((0, 0, 0), np.float32)

        for i in range(len(index) // 3):
            triangle = []
            for j in range(3):
                triangle.append(position[index[3 * i + j]])
            
            triangle_normal = normal_vec(triangle[0], triangle[1], triangle[2])
            for j in range(3):
                normal[index[3 * i + j]] += triangle_normal
        
        for i in range(dim_total):
            normal[i] = normalized(normal[i])
                
        attributes = dict(position=position, normal=normal)

        super().__init__(shader, attributes=attributes, index=index, **uniforms)


def fmod1(i, v):
    if i >= 0:
        return 1 - abs(2 * v - 1)
    return v

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("texture.vert", "texture.frag")
    height_map_shader = Shader("height_map_default.vert", "height_map_default.frag")
    lava_shader = Shader("lava_default.vert", "lava_default.frag")
    
    """
    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])

    if len(sys.argv) != 2:
        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))
        viewer.add(TexturedPlane(shader, "100.png"))
    """

    # heightmap test with perlin noise
    dim = (100, 100)
    res = (1000, 1000)
    crater_rayon = .2
    reso = max(res)
    ratata = make_random_grid(dim, 0, 1)
    height = np.ndarray(res, float)
    ampl = [.5, 2, 4, 8, 8, 8]
    freq = [64, 32, 16, 8, 4, 2]
    lava_height = .01

    for i in range(res[0]):
        for j in range(res[1]):
            x = i / reso
            y = j / reso
            rayon = (x - .5) ** 2 + (y - .5) ** 2
            scaled_perlin = (perlin(ratata, [x, y], ampl, freq, fmod=fmod1) - .5) * .4
            (volc, no) = volcano(rayon, .05, .1, .2)
            height[i, j] = volc * .3 + (1 - no) * scaled_perlin

    height_unif = {"lava_height":lava_height}
    new_map = HeightMap(height_map_shader, height, **height_unif)

    lava_grid = np.ones((2, 2), np.float32)
    lava_grid *= lava_height
    lava_map = HeightMap(lava_shader, lava_grid)

    viewer.add(lava_map)
    viewer.add(new_map)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
