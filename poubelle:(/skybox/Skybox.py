"""Defining Skybox class which is inspired by Textured plane"""
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured

class FreePlane(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file, base_coords):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        # setup plane mesh to be textured
        scaled = 5 * np.array(base_coords, np.float32)
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

class Skybox():
    def __init__(self, texfiles:list):
        """
        texfiles must be in this order : [top, bottom, left, right, front, back]
        """
        top_bottom_shader = Shader("texturetop_bottom.vert", "texture.frag")
        self.faces = []
        top_coord = ((-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1))
        top = FreePlane(top_bottom_shader, texfiles[0], top_coord)
        self.faces.append(top)

        bottom_coord = ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0))
        bottom = FreePlane(top_bottom_shader, texfiles[1], bottom_coord)
        self.faces.append(bottom)

        left_right_shader = Shader("textureleft_right.vert", "texture.frag")
        left_coord = ((-1, -1, 0), (1, -1, 0), (1, -1, 1), (-1, -1, 1))
        left = FreePlane(left_right_shader, texfiles[2], left_coord)
        self.faces.append(left)

        right_coord = ((1, 1, 0), (1, 1, 1), (-1, 1, 1), (-1, 1, 0))
        right = FreePlane(left_right_shader, texfiles[3], right_coord)
        self.faces.append(right)

        front_back_shader = Shader("texturefront_back.vert", "texture.frag")
        front_coord = ((-1, -1, 0), (-1, -1, 1), (-1, 1, 1), (-1, 1, 0))
        front = FreePlane(front_back_shader, texfiles[4], front_coord)
        self.faces.append(front)

        back_coord = ((1, -1, 0), (1, -1, 1), (1, 1, 1), (1, 1, 0))
        back = FreePlane(front_back_shader, texfiles[5], back_coord)
        self.faces.append(back)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        for face in self.faces:
            face.draw(primitives, **uniforms)
