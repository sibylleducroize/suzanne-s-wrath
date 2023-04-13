#version 330 core

uniform mat4 projection;
uniform mat4 view;

in vec3 position;

out vec3 tex_coords;

void main() {
    mat4 new_view = mat4(mat3(view)); //on ote les translations pour la skybox
    tex_coords = position;
    gl_Position = projection * new_view * vec4(position, 1.0);
} 
