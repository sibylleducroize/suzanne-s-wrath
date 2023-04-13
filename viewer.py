#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from skybox_material import MaterialCubemap
from cube import Cube


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("skybox.vert", "skybox.frag")

    viewer.add(MaterialCubemap("gfx/sky", Cube(shader)))
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
