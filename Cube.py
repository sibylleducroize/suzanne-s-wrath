import OpenGL.GL as gl
import numpy as np
from core import Mesh, Shader
from texture import Texture, Textured


class Cube(Mesh):
    """Mesh of a cube that can be seen from inside"""

    def __init__(self, shader):
        position = np.array(((-1, -1, -1),  # 0,E
                            (1, -1, -1),  # 1, F
                            (1, 1, -1),  # 2, G
                            (-1, 1, -1),  # 3, H
                            (-1, -1, 1),  # 4, A
                            (1, -1, 1),  # 5, D
                            (1, 1, 1),  # 6, C
                            (-1, 1, 1)),
                            np.float32  # 7, B
                            )
        indices = np.array((3, 7, 4,
                            4, 0, 3,  # back
                            2, 6, 3,
                            3, 6, 7,  # right
                            1, 5, 2,
                            2, 5, 6,  # front
                            0, 4, 5,
                            5, 1, 0,  # left
                            4, 7, 5,
                            5, 7, 6,  # top
                            1, 3, 0,
                            3, 1, 2), np.uint32)
        color = np.array(((1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),
                         (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0)), 'f')
        self.color = (1, 1, 0)
        attributes = dict(position=position, color=color)
        super().__init__(shader, attributes=attributes, index=indices)

    def draw(self, primitives=gl.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, **uniforms)

    def key_handler(self, key):
        if key == glfw.KEY_C:
            self.color = (0, 0, 0)


class Cube_Textured():
    def __init__(self, shaders:list, textures_path:list):
        """Shaders must be in this order : 
        front, back, left, right, top, bottom"""
        self.textured_faces = []
        # Declaring all vertexes of the figure
        position = np.array(((-1, -1, -1),  # 0,E
                             (1, -1, -1),  # 1, F
                             (1, 1, -1),  # 2, G
                             (-1, 1, -1),  # 3, H
                             (-1, -1, 1),  # 4, A
                             (1, -1, 1),  # 5, D
                             (1, 1, 1),  # 6, C
                             (-1, 1, 1)),
                            np.float32  # 7, B
                            )
        # Only puting in indexes the positions used for each face
        indices_back = np.array((3, 7, 4, 4, 0, 3), np.uint32)
        indices_right = np.array((2, 6, 3, 3, 6, 7), np.uint32)
        indices_front = np.array((1, 5, 2, 2, 5, 6), np.uint32)
        indices_left = np.array((0, 4, 5, 5, 1, 0), np.uint32)
        indices_top = np.array((4, 7, 5, 5, 7, 6), np.uint32)
        indices_bottom = np.array((1, 3, 0,3, 1, 2), np.uint32)
        
        #creating meshes
        front = Mesh(shaders[0], attributes=dict(position=position), index=indices_front)
        back = Mesh(shaders[1], attributes=dict(position=position), index=indices_back)
        left = Mesh(shaders[2], attributes=dict(position=position), index=indices_left)
        right = Mesh(shaders[3], attributes=dict(position=position), index=indices_right)
        top = Mesh(shaders[4], attributes=dict(position=position), index=indices_top)
        back = Mesh(shaders[5], attributes=dict(position=position), index=indices_bottom)

        #creating textured surfaces
        front_textured = Textured(front, diffuse_map = Texture(textures_path[0], wrap_mode=gl.GL_CLAMP_TO_EDGE, min_filter=gl.GL_LINEAR))
        back_textured = Textured(back, diffuse_map = Texture(textures_path[1], wrap_mode=gl.GL_CLAMP_TO_EDGE))
        left_textured = Textured(left, diffuse_map = Texture(textures_path[2], wrap_mode=gl.GL_CLAMP_TO_EDGE))
        right_textured = Textured(right, diffuse_map = Texture(textures_path[3], wrap_mode=gl.GL_CLAMP_TO_EDGE))
        top_textured = Textured(top, diffuse_map = Texture(textures_path[4], wrap_mode=gl.GL_CLAMP_TO_EDGE))
        back_textured = Textured(back, diffuse_map = Texture(textures_path[5], wrap_mode=gl.GL_CLAMP_TO_EDGE))

        self.textured_faces.append(front_textured)
        self.textured_faces.append(back_textured)
        self.textured_faces.append(left_textured)
        self.textured_faces.append(right_textured)
        self.textured_faces.append(top_textured)
        self.textured_faces.append(back_textured)

        #initializing debug things
        self.color = (1, 1, 1)
    
    def draw(self, primitives=gl.GL_TRIANGLES, **uniforms):
        for face in self.textured_faces:
            face.draw(primitives = primitives, **uniforms)
