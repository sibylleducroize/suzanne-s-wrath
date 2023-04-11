#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured
from Cube import Cube_Textured


    
# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader_front_back = Shader("texturefront_back.vert", "texture.frag")
    shader_left_right = Shader("textureleft_right.vert", "texture.frag")
    shader_top_bottom = Shader("texturetop_bottom.vert", "texture.frag")
    shaders = [shader_front_back, shader_front_back, shader_left_right, shader_left_right, shader_top_bottom, shader_top_bottom]
    textures_path = ["skybox_pics/front.jpg", "skybox_pics/back.jpg", "skybox_pics/left.jpg",
                     "skybox_pics/right.jpg", "skybox_pics/top.jpg", "skybox_pics/bottom.jpg"]

    viewer.add(Cube_Textured(shaders, textures_path));
    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
