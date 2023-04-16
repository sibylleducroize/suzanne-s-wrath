#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured
from transform import normalized, normal_vec, translate, scale, identity, lookat
from math import exp, pi
from random import uniform

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
        The scaling applied is the same on both the x and z axis."""
    def __init__(self, shader, grid, bonus_attrib=None, usage=GL.GL_STATIC_DRAW, **uniforms):
        # grid should be a numpy array
        dim = grid.shape
        dimax = max(dim) - 1
        ratio = 2 / dimax
        dim_total = dim[0] * dim[1]

        vertex_list = []
        for i in range(dim[0]):
            for j in range(dim[1]):
                x = i * ratio - 1
                z = j * ratio - 1
                y = grid[i, j]
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
                    dx = (dx + dp) % 2
                    dy = (dy + dp + 1) % 2

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
        if bonus_attrib != None:
            attributes[bonus_attrib[0]] = bonus_attrib[1]

        super().__init__(shader, attributes=attributes, index=index, usage=usage, **uniforms)


class Lava():
    def __init__(self, shader, viewer, **unifs):
        self.dim = (2, 2)
        self.speed = .01
        self.len = self.dim[0] * self.dim[1]
        self.unif = unifs
        self.viewer = viewer
        text = Texture("gud.png", GL.GL_REPEAT)
        lava_map = unifs.get("lava_height") * np.ones(self.dim, np.float32)
        self.uvmap = []
        for i in range(self.len):
            self.uvmap.append((i % 2, i // 2))
        self.uvmap = 10 * np.array(self.uvmap, np.float32)
        drawable = HeightMap(shader, lava_map, bonus_attrib=("uv_map", self.uvmap), **unifs)
        self.time = 0
        self.drawable = Textured(drawable, lava_tex=text)

    
    def draw(self, **balec):
        nt = self.viewer.time
        dt = nt - self.time
        self.time = nt
        p = self.speed * self.time

        t1 = np.matrix(((1, 0, p),
                        (0, 1, 0),
                        (0, 0, 1)))
        t2 = np.matrix(((1/pi, 0, -p),
                        (0, 1/pi, 0),
                        (0, 0, 1)))

        self.drawable.draw(trans1=t1, trans2=t2, **balec)

class Skaibocs(Textured):
    """ I am have cancer """

    def __init__(self, shader):
        position = 100 * np.array(((-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
                             (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                             (-1, -1, -1), (-1, 1, -1),
                             (1, 1, -1), (1, 1, 1),
                             (1, -1, -1), (1, -1, 1)), np.float32)
        index = np.array((0, 1, 2, 2, 3, 0,
                          7, 6, 5, 5, 4, 7,
                          1, 5, 6, 6, 2, 1,
                          4, 8, 9, 9, 7, 4,
                          7, 9, 10, 10, 11, 7,
                          8, 4, 13, 13, 12, 8), np.uint32)

        q = .25
        t = 1/3
        marge = 0.0001
        uv_map = np.array(((0, 2 * t - marge), (q, 2 * t - marge), (q, t + marge), (0, t + marge),
                           (3 * q + marge, 2 * t - marge), (2 * q, 2 * t - marge), (2 * q, t + marge), (3 * q + marge, t + marge),
                           (4 * q, 2 * t), (4 * q, t),
                           (1 + marge, 0), (3 * q + marge, 0),
                           (1 + marge, 1), (3 * q + marge, 1)), np.float32)
        tex = Texture("skabock4.jpg", GL.GL_CLAMP_TO_EDGE)
        attributes = dict(position=position, tex_coord=uv_map)
        mesh = Mesh(shader, attributes=attributes, index=index)

        super().__init__(mesh, test_texure=tex)


class Particle:
    def __init__(self, drawable, speed):
        self.drawable = drawable
        self.pos = np.array((uniform(-1, 1), uniform(0, 1), uniform(-1, 1)), np.float32)
        self.speed = speed
        self.up = np.array((0, 1, 0), np.float32)
    
    def update(self, dt):
        self.pos[1] -= self.speed * dt
        if self.pos[1] < 0:
            self.pos[1] = 1
            self.pos[0], self.pos[2] = uniform(-1, 1), uniform(-1, 1)
        
    def draw(self, dt, **kws):
        self.update(dt)
        self.drawable.draw(part_pos = self.pos, **kws)


class Ashes:
    def __init__(self, shader, number, size, viewer, **kws):
        self.particle_list = np.ndarray((number), Particle)
        position = size * np.array(((0, 0, 0), (0, -1, 0), (1, 0, 0), (0, 1, 0), (-1, 0, 0)), np.float32)
        index = np.array((0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 1))
        attributes = dict(position=position)
        losange = Mesh(shader, attributes=attributes, index=index)
        for i in range(number):
            self.particle_list[i] = Particle(losange, uniform(.01, .1))
        self.time = 0
        self.kws = kws
        self.viewer = viewer
        
    def draw(self, **kws):
        dt = self.viewer.time - self.time
        self.time = self.viewer.time
        for part in self.particle_list:
            part.draw(dt, **kws, **self.kws)


def fmod1(i, v):
    if i >= 0:
        return 1 - abs(2 * v - 1)
    return v

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    height_map_shader = Shader("height_map_default.vert", "height_map_default.frag")
    lava_shader = Shader("lava_default.vert", "lava_default.frag")
    test_shader = Shader("text_default.vert", "text_default.frag")
    ashes_shader = Shader("ashes_default.vert", "ashes_default.frag")
    lava_shader2 = Shader("lava2.vert", "lava2.frag")

    # heightmap with perlin noise
    dim = (100, 100)
    res = (1000, 1000)
    crater_rayon = .2
    reso = max(res)
    ratata = make_random_grid(dim, 0, 1)
    height = np.ndarray(res, float)
    ampl = [.5, 2, 4, 8, 8, 8]
    freq = [64, 32, 16, 8, 4, 2]
    lava_height = .01
    fog_strength = .3
    max_fog = 1
    fog_height = .3

    for i in range(res[0]):
        for j in range(res[1]):
            x = i / reso
            y = j / reso
            rayon = (x - .5) ** 2 + (y - .5) ** 2
            scaled_perlin = (perlin(ratata, [x, y], ampl, freq, fmod=fmod1) - .5) * .4
            (volc, no) = volcano(rayon, .05, .1, .2)
            height[i, j] = volc * .3 + (1 - no) * scaled_perlin

    height_unif = {"lava_height":lava_height, "fog_strength":fog_strength, "max_fog":max_fog, "fog_height":fog_height}
    new_map = HeightMap(height_map_shader, height, **height_unif)

    #lava
    #lava_grid = np.ones((2, 2), np.float32)
    #lava_grid *= lava_height
    #lava_unif = {"fog_strength":fog_strength, "max_fog":max_fog}
    #lava_map = HeightMap(lava_shader, lava_grid, **lava_unif)
    lava_map = Lava(lava_shader2, viewer, lava_height=lava_height, fog_strength=fog_strength, max_fog=max_fog, fog_height=fog_height)
    viewer.add(lava_map)
    

    #skybox
    test_sky_box = Skaibocs(test_shader)

    viewer.add(test_sky_box)
    viewer.add(lava_map)
    viewer.add(new_map)

    #ashes
    ashes = Ashes(ashes_shader, 400, .0015, viewer, **height_unif)
    viewer.add(ashes)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
