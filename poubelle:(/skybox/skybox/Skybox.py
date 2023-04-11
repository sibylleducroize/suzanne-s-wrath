import OpenGL.GL as gl
import numpy as np
import urllib.request
from PIL import Image
from core import Mesh, Shader
from texture import Textured
from Cube import Cube

class Skybox():
    def __init__(self, textures):
        self.shader = Shader("skybox/skybox.vert", "skybox/skybox.frag")

        # On crée le mesh ie le cube
        self.drawable = Cube(self.shader)
        # On crée les texture
        self.glid = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.glid)

        for i in range(len(textures)):
            img = Image.open(textures[i])
            img_data = np.array(list(img.getdata()), np.uint8)

            gl.glTexImage2D(gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
                            0, gl.GL_RGB, img.width, img.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_data)

        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)

    def draw(self, primitives=gl.GL_TRIANGLES, **uniforms):
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.glid)
        self.drawable.draw()

"""
class Skybox(Mesh):
    def __init__(self, faces: list):
        faces: right, left, top, bottom, front, back
        self.glid = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.glid)

        for i in range(len(faces)):
            response = urllib.request.urlopen(faces[i])
            img = Image.open(response)
            img_data = np.array(list(img.getdata()), np.uint8)

            gl.glTexImage2D(gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
                            0, gl.GL_RGB, img.width, img.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_data)

        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)

    def __del__(self):  # delete GL texture from GPU when object dies
        gl.glDeleteTextures(self.glid)
"""
    




