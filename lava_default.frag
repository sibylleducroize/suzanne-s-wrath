#version 330 core

// global color variable
//uniform vec3 global_color;
uniform float fog_strength;
uniform float max_fog;

// receiving interpolated color for fragment shader
in vec3 fragment_color;
in vec3 fragment_normal;
in float depth;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    //out_color = vec4(fragment_color + global_color, 1);
    vec4 color = vec4(.95, .1, .1, 1);
    //float fog_factor = max_fog * (1 - exp(-depth * fog_strength));
    //color = fog_factor * vec4(.2, .2, .2, 1) + (1 - fog_factor) * color;
    out_color = color;
}
