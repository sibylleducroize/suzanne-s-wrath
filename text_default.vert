#version 330 core

// input attribute variable, given per vertex
in vec3 position;
in vec3 normal;
in vec2 tex_coord;

// global matrix variables
uniform mat4 view;
uniform mat4 projection;
uniform vec3 camera_position;

// interpolated color for fragment shader, intialized at vertices
out vec2 fragment_tex_coord;

void main() {
    // initialize interpolated colors at vertices
    fragment_tex_coord = tex_coord;

    // tell OpenGL how to transform the vertex to clip coordinates
    gl_Position = projection * vec4(mat3(view) * position, 1);
}
