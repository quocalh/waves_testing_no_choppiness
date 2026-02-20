// VERTEX SHADER
#version 330 core

layout (location = 0) in vec3 in_Position;

#define WAVES_NUMBER 50
#define G 9.81
#define wind_speed 30
#define philips_constant 10
const vec2 wind_direction = vec2(cos(20), sin(20));
const float sqrt_2 = sqrt(2);

out vec3 position;
out vec3 normal;

uniform mat4 perspective_mat;
uniform float time;

void main()
{
    float u = in_Position.x;
    float v = in_Position.z;
    vec2 uv = vec2(u,v);

    float a;
    float w; // this is the speed of the wave, not frequency
    vec2 wave_vector;
    vec2 k; // frequency here (wave_vector magnitude)
    vec2 wave_direction; // wave_vector direction

    vec3 parametric_position = vec3(u, 0, v);
    normal = vec3(0, 1, 0);

    float wind_direction;
    float wind_speed;
    float philips;
    float 

    for (int i = 0; i < WAVES_NUMBER; i++)
    {   
            // get wave vector (wave dir * frequency)
        wave_vector = ;
        k = length(wave_vector);    // get frequency
        wave_direction = wave_vector / k;

            // get w (speed)
        w = sqrt(G * k);
        
            // phillips spectrum
        float exponent = -1 / pow(k * wind_speed * wind_speed / G, 2);
        philips = philips_constant *  exp(exponent) / (k * k * k * k);
        philips *= dot(wind_direction, wave_direction) * dot(wind_direction, wave_direction);

            // amplitude (temporarily disregard the Guassian complex term)
        a = 1 / sqrt_2 * sqrt(philips);

        parametric_position += vec3(
            - a * wave_vector.x / k * cos(dot(wave_vector, uv) - w * time + wave_vector.x),
              a *                     sin(dot(wave_vector, uv) - w * time + wave_vector.x),
            - a * wave_vector.y / k * cos(dot(wave_vector, uv) - w * time + wave_vector.x)
        );

        normal += vec3(
            - wave_vector.x * a * cos(dot(wave_vector, uv) - w * time + wave_vector.x),
            - k             * a * sin(dot(wave_vector, uv) - w * time + wave_vector.x),
            - wave_vector.y * a * cos(dot(wave_vector, uv) - w * time + wave_vector.x)
        );

    }
    normal = normalize(normal);

    gl_Position = perspective_mat * vec4(parametric_position, 1.0);
    position = parametric_position;
}

// FRAGMENT SHADER
#version 330 core

in vec3 normal;
in vec3 position;


uniform vec3 water_color;
uniform vec3 light_pos;
uniform vec3 cam_pos;
uniform vec3 sky_color;

out vec4 glFragColor;


const vec3 upwelling = vec3(0, 0.2, 0.3);
const vec3 sky =  vec3(0.69, 0.84, 1);
const vec3 air = vec3(0.1, 0.1, 0.1);
const float nSnell = 1.34;
const float Kdiffuse = 0.91;

void main()
{
    vec3 light_dir = normalize(light_pos - position);
    vec3 eye_dir = normalize(cam_pos - position);

    float reflectivity;
    float cos_i = clamp(dot(normal, eye_dir), 0.0, 1.0);
    float incident_rad = acos(cos_i);

    float sin_i = sin(incident_rad);
                // ni sin(0i) = nt sin(0t);
                // 1 sin(0i) = 4/3 sin(0t);
                // 3/4 sin(0i) = sin(0t);
    float sin_t = 0.75 * sin_i;
    transmision_rad = asin(sin_t);

    float a = sin(transmision_rad - incident_rad) / sin(transmision_rad + incident_rad);
    float b = tan(transmision_rad - incident_rad) / tan(transmision_rad + incident_rad);

    reflectivity = 0.5 * (a * a + b * b);
    float transmissivity = 1 - reflectivity;

    float distance = length(position - cam_pos) * Kdiffuse;
    distance = exp(-distance);

    vec3 color = distance * (
        reflectivity * sky + (1 - reflectivity) * upwelling
    ) + (1 - distance) * air;

    // no foam just yet

    glFragColor = vec4(color, 0.5);
}