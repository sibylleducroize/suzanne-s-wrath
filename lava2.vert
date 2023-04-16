#version 330 core

// input attribute variable, given per vertex
in vec3 position;
in vec2 uv_map;

// global matrix variables
uniform mat4 view;
uniform mat4 projection;
uniform vec3 camera_position;
uniform float time;
uniform float speed;
uniform mat3 trans1;
uniform mat3 trans2;
uniform mat3 trans3;

// interpolated color for fragment shader, intialized at vertices
out vec2 fragment_tex_coord1;
out vec2 fragment_tex_coord2;
out vec3 fragment_position;

void main() {
    // initialize interpolated colors at vertices
    fragment_tex_coord1 = vec2(trans1 * vec3(uv_map, 1));
    fragment_tex_coord2 = vec2(trans2 * vec3(uv_map, 1));
    fragment_position = position;

    // tell OpenGL how to transform the vertex to clip coordinates
    gl_Position = projection * view * vec4(position, 1);
}
