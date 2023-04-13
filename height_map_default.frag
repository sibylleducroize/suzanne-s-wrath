#version 330 core

// global color variable
//uniform vec3 global_color;
uniform float lava_height;
uniform float fog_strength;
uniform float max_fog;
uniform float fog_height;
uniform vec3 camera_position;

// receiving interpolated color for fragment shader
in vec3 fragment_color;
in vec3 fragment_normal;
in vec3 fragment_position;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    //out_color = vec4(fragment_color + global_color, 1);
    
    float intensity = dot(fragment_normal, normalize(vec3(1, 1, 0)));
    float redtensity = exp(-3000 * (fragment_position.y - lava_height) * (fragment_position.y - lava_height));
    vec4 color = vec4(intensity * fragment_color, 1);
    color.x += redtensity;

    float depth = 0;
    if ((camera_position.y >= fog_height) && (fragment_position.y >= fog_height)) {
        depth = 0;
    }
    else if ((camera_position.y < fog_height) && (fragment_position.y < fog_height)) {
        depth = length(camera_position - fragment_position);
    }
    else if (camera_position.y > fog_height) {
        depth = length(camera_position - fragment_position);
        depth *= (fog_height - fragment_position.y) / (camera_position.y - fragment_position.y);
    }
    else {
        depth = length(camera_position - fragment_position);
        depth *= (fog_height - camera_position.y) / (fragment_position.y - camera_position.y);
    }

    float fog_factor = max_fog * (1 - exp(-depth * fog_strength));
    color = fog_factor * vec4(.7, .08, .08, 1) + (1 - fog_factor) * color;
    out_color = color;
    //out_color = vec4(fragment_normal, 1);
}
