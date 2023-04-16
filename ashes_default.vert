#version 330 core

// input attribute variable, given per vertex
in vec3 position;

// global matrix variables
uniform vec3 part_pos;
uniform float part_size;
uniform mat4 view;
uniform mat4 projection;
uniform vec3 camera_position;

// interpolated color for fragment shader, intialized at vertices
out vec3 fragment_position;
void main() {
    // initialize interpolated colors at vertices
    vec3 direction = normalize(camera_position - part_pos);
    mat4 transform;
    transform[2] = vec4(direction, 0);
    transform[0] = vec4(normalize(vec3(direction[2], 0, -direction[0])), 0);
    transform[1] = vec4(normalize(cross(direction, vec3(transform[0]))), 0);
    transform[3] = vec4(part_pos, 1);

    // tell OpenGL how to transform the vertex to clip coordinates
    vec4 inter_pos = transform * vec4(position, 1);
    fragment_position = vec3(inter_pos);
    gl_Position = projection * view * inter_pos;
}
