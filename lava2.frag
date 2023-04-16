#version 330 core

// global color variable
//uniform vec3 global_color;
uniform sampler2D lava_tex;
uniform float fog_height;
uniform float fog_strength;
uniform float max_fog;
uniform vec3 camera_position;

// receiving interpolated color for fragment shader
in vec2 fragment_tex_coord1;
in vec2 fragment_tex_coord2;
in vec3 fragment_position;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    vec4 color = vec4(0, 0, 0, 1);
    color += texture(lava_tex, fragment_tex_coord1);
    color += texture(lava_tex, fragment_tex_coord2) * 2;
    color = color / 2 + vec4(.5, .1, .1, 1);

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
}
