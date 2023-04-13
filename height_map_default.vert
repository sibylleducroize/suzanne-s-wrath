#version 330 core

// input attribute variable, given per vertex
in vec3 position;
in vec3 normal;

// global matrix variables
uniform mat4 view;
uniform mat4 projection;
uniform vec3 camera_position;

// interpolated color for fragment shader, intialized at vertices
out vec3 fragment_color;
out vec3 fragment_normal;
out vec3 fragment_position;

void main() {
    // initialize interpolated colors at vertices
    vec3 base_color;
    if (normal.y < .8) {
        base_color = vec3(.3, .3, .3);
    }
    else {
        base_color = vec3(.5, .5, .5);
    }
    fragment_color = base_color;
    fragment_normal = normal;
    fragment_position = position;

    // tell OpenGL how to transform the vertex to clip coordinates
    gl_Position = projection * view * vec4(position, 1);
}
