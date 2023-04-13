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