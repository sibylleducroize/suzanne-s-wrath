#version 330 core

// global color variable
//uniform vec3 global_color;
uniform float fog_strength;
uniform float max_fog;
uniform sampler2D test_texture;

// receiving interpolated color for fragment shader
in vec2 fragment_tex_coord;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    out_color = texture(test_texture, fragment_tex_coord);
}
