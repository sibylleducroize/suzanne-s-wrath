#version 330 core

// global color variable
//uniform vec3 global_color;
uniform float lava_height;

// receiving interpolated color for fragment shader
in vec3 fragment_color;
in vec3 fragment_normal;
in vec3 fragment_position;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    //out_color = vec4(fragment_color + global_color, 1);
    
    float intensity = dot(fragment_normal, normalize(vec3(1, 0, 1)));
    float redtensity = exp(-3000 * (fragment_position.z - lava_height) * (fragment_position.z - lava_height));
    vec4 color = vec4(intensity * fragment_color, 1);
    color.x += redtensity;
    out_color = color;
    //out_color = vec4(fragment_normal, 1);
}
