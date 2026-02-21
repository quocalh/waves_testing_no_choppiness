// VERTEX SHADER
#version 330 core

layout (location = 0) in vec3 in_Position;

#define WAVES_NUMBER 190
#define G 9.81
#define wind_speed 2
#define philips_constant 2
const vec2 wind_direction = vec2(cos(20), sin(20));
const float sqrt_2 = sqrt(2);

out vec3 position;
out vec3 normal;

// const vec2 uniform_distributed_vectors[2] = vec2[2](
//     vec2(-0.9703, -0.2421),
//     vec2(0.7318, 0.6815)
// );
const vec2 uniform_distributed_vectors[200] = vec2[200](
    vec2(-32.0955, -37.2671),
    vec2(-46.8885, 2.2765),
    vec2(62.0853, 2.2981),
    vec2(10.8392, -22.2288),
    vec2(-19.4388, -32.3327),
    vec2(-0.1634, 2.6839),
    vec2(4.0197, -6.9808),
    vec2(-41.6574, 19.0725),
    vec2(14.6918, 62.4381),
    vec2(52.3449, 32.1644),
    vec2(-41.2522, -55.7429),
    vec2(33.8797, -31.2726),
    vec2(23.1650, 0.3702),
    vec2(4.9639, -16.5416),
    vec2(-50.3346, 11.5284),
    vec2(-16.7167, 14.9781),
    vec2(-77.6992, 43.0625),
    vec2(30.8747, -85.8280),
    vec2(59.8256, -25.9095),
    vec2(35.4674, 63.8697),
    vec2(3.8017, 2.6636),
    vec2(33.7059, -79.3222),
    vec2(0.2013, 3.9101),
    vec2(15.0653, -59.6599),
    vec2(31.4871, 61.9002),
    vec2(-90.9676, 32.1476),
    vec2(-2.4717, -25.8309),
    vec2(34.7726, -79.2535),
    vec2(29.6776, 43.6081),
    vec2(45.5308, 11.3499),
    vec2(95.5220, -25.5885),
    vec2(36.4130, -12.3567),
    vec2(-59.0644, -41.2125),
    vec2(-54.1059, 11.8839),
    vec2(-16.6207, 57.7605),
    vec2(-7.9985, 12.0412),
    vec2(-60.5450, -6.7451),
    vec2(-45.1403, 31.2854),
    vec2(31.5771, -21.7126),
    vec2(-13.0352, -35.2178),
    vec2(-34.7680, 5.2977),
    vec2(12.7402, -47.3841),
    vec2(-0.4899, -0.5106),
    vec2(11.3284, -29.5034),
    vec2(14.9244, 12.0286),
    vec2(52.2330, 55.0083),
    vec2(47.0512, 40.6771),
    vec2(5.6488, -64.6177),
    vec2(-31.8494, -0.6607),
    vec2(30.9222, -86.9771),
    vec2(-3.7783, 83.2500),
    vec2(-10.6527, -53.6393),
    vec2(37.7470, 6.0901),
    vec2(-32.7205, 16.0888),
    vec2(80.1941, 17.8336),
    vec2(-26.5863, 19.3598),
    vec2(34.0507, 21.5309),
    vec2(4.7497, 13.6227),
    vec2(2.8319, -16.8988),
    vec2(61.1393, -50.6194),
    vec2(27.1317, 8.8139),
    vec2(-21.4617, 92.3725),
    vec2(42.8423, -32.6346),
    vec2(71.3245, 9.9637),
    vec2(-8.4408, 48.9124),
    vec2(1.6916, 71.9594),
    vec2(20.3273, 7.8285),
    vec2(4.3743, -0.2426),
    vec2(-58.9121, 28.0886),
    vec2(14.4662, 7.9448),
    vec2(-13.8780, -87.6279),
    vec2(37.6609, 31.8551),
    vec2(71.2941, -5.2143),
    vec2(36.8230, 0.7937),
    vec2(-43.8667, -60.2917),
    vec2(87.3866, 11.8358),
    vec2(-17.9509, 13.0223),
    vec2(-0.8099, 0.4653),
    vec2(-46.7272, -34.2293),
    vec2(20.2828, -59.2380),
    vec2(-37.2068, -88.5461),
    vec2(-23.7558, 29.5360),
    vec2(2.1571, -99.0315),
    vec2(-55.7940, 2.4998),
    vec2(-17.0945, -38.0126),
    vec2(46.2135, -37.8705),
    vec2(43.0217, 66.3844),
    vec2(-55.5632, 40.9694),
    vec2(-7.7212, 32.0239),
    vec2(9.4316, -1.3317),
    vec2(25.0225, -76.7256),
    vec2(83.7925, -48.6285),
    vec2(-10.4865, 12.0507),
    vec2(23.6970, 12.4510),
    vec2(-18.6861, -42.1166),
    vec2(-2.1859, -10.8511),
    vec2(22.4441, -58.6245),
    vec2(25.9288, 49.6662),
    vec2(-54.7727, 51.1965),
    vec2(5.8959, 5.3815),
    vec2(40.0165, 20.9716),
    vec2(-40.8574, 71.8372),
    vec2(-82.5361, 13.4162),
    vec2(-50.7209, 35.2261),
    vec2(-1.0599, 3.7537),
    vec2(-0.5040, -4.3019),
    vec2(-9.5378, 14.8817),
    vec2(-37.5023, -0.6870),
    vec2(-8.1147, 11.1742),
    vec2(-2.7739, -9.4501),
    vec2(75.8449, -39.2518),
    vec2(59.5178, -70.5557),
    vec2(29.3056, 2.6691),
    vec2(66.5985, 27.3785),
    vec2(-70.6473, -27.6659),
    vec2(31.2656, -11.5334),
    vec2(6.0001, -8.2775),
    vec2(-60.4860, 16.2524),
    vec2(-31.5153, -57.5343),
    vec2(-36.2548, 23.4973),
    vec2(-19.0612, -4.2880),
    vec2(-71.1348, -8.8640),
    vec2(-6.3664, -97.4474),
    vec2(43.6818, -83.7555),
    vec2(4.1734, -0.6546),
    vec2(2.5405, -60.4134),
    vec2(-4.8338, 15.8016),
    vec2(-5.5341, 15.8326),
    vec2(-76.2704, 5.3826),
    vec2(-25.3189, 31.5916),
    vec2(-0.3770, -0.3146),
    vec2(-50.3184, -35.8353),
    vec2(-48.7120, 31.4702),
    vec2(-46.8875, 55.6981),
    vec2(0.4619, 33.2746),
    vec2(-4.9016, -2.8027),
    vec2(-35.8597, 78.5568),
    vec2(1.6524, -21.7607),
    vec2(-74.0238, -39.5181),
    vec2(77.4099, 48.0693),
    vec2(-41.5046, -68.6430),
    vec2(-28.8866, -60.5550),
    vec2(-18.2661, 40.3575),
    vec2(74.1355, 7.7913),
    vec2(-36.6158, 39.1965),
    vec2(14.2542, -59.6166),
    vec2(-29.9440, 19.5533),
    vec2(24.1183, 12.8110),
    vec2(-35.0142, 50.4620),
    vec2(-2.3625, -2.6232),
    vec2(-3.9728, -6.8773),
    vec2(15.7463, -19.2341),
    vec2(-9.5014, 40.8112),
    vec2(-69.0474, -20.8852),
    vec2(65.7978, -38.7927),
    vec2(2.9003, -31.7515),
    vec2(0.1963, 16.8256),
    vec2(-0.4754, -49.4168),
    vec2(-6.9758, 39.3214),
    vec2(-14.8777, 29.6560),
    vec2(-49.0396, 84.7151),
    vec2(-30.1835, 14.8069),
    vec2(-50.1904, 27.0800),
    vec2(-3.2344, 21.5475),
    vec2(84.7360, -49.6876),
    vec2(-61.3614, -56.3653),
    vec2(2.5337, 2.0549),
    vec2(36.5135, 3.2030),
    vec2(-24.3571, -41.8811),
    vec2(42.9075, 49.9386),
    vec2(-3.6462, 76.1618),
    vec2(48.2921, 3.4568),
    vec2(28.4316, -7.6856),
    vec2(5.5979, 7.8852),
    vec2(-25.8280, -54.4639),
    vec2(35.2286, -73.0590),
    vec2(-46.8806, -30.1008),
    vec2(-77.3187, -24.8968),
    vec2(-40.9124, 70.8079),
    vec2(-2.2811, -61.4387),
    vec2(56.4553, -56.7828),
    vec2(5.4009, -11.2829),
    vec2(-81.1542, 20.3462),
    vec2(6.2168, -10.1355),
    vec2(-69.2546, 18.0370),
    vec2(-19.7065, 72.0175),
    vec2(-45.0785, 42.5415),
    vec2(2.7099, 2.3855),
    vec2(-22.4573, 65.2733),
    vec2(30.5484, -22.0540),
    vec2(41.2354, 58.7231),
    vec2(50.3769, -14.9978),
    vec2(6.2609, -23.6205),
    vec2(16.1010, -49.6573),
    vec2(18.1249, -5.3084),
    vec2(-39.9055, -73.3668),
    vec2(19.0934, -21.9987),
    vec2(25.6960, -3.9880),
    vec2(-22.5597, -9.2084),
    vec2(0.2665, -9.4954)
);

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
    float k; // frequency here (wave_vector magnitude)
    vec2 wave_direction; // wave_vector direction

    vec3 parametric_position = vec3(u, 0, v);
    normal = vec3(0, 1, 0);

    float philips;

    for (int i = 0; i < WAVES_NUMBER; i++)
    {   
            // get wave vector (wave dir * frequency)
        wave_vector = uniform_distributed_vectors[i];
        k = length(wave_vector);    // get frequency
        wave_direction = wave_vector / k;
        // k = pow(1 * k, 1.15);

            // get w (speed)
        w = sqrt(G * k);
        w = 0.3 * w;
        
            // phillips spectrum
        float exponent = -1 / pow(k * wind_speed * wind_speed / G, 2);
        philips = philips_constant *  exp(exponent) / (k * k * k * k);
        philips *= dot(wind_direction, wave_direction) * dot(wind_direction, wave_direction);

            // amplitude (temporarily disregard the Guassian complex term)
        a = 1 / sqrt_2 * sqrt(philips);
        a = pow(a, 1.2);

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


const vec3 upwelling = vec3(0.1, 0.2, 0.4);
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
    float transmision_rad = asin(sin_t);

    float a = sin(transmision_rad - incident_rad) / sin(transmision_rad + incident_rad);
    float b = tan(transmision_rad - incident_rad) / tan(transmision_rad + incident_rad);

    reflectivity = 0.5 * (a * a + b * b);
    float transmissivity = 1 - reflectivity;

    float distance = length(position - cam_pos) * Kdiffuse;
    distance = exp(-distance / 10);
    distance = 1;

    vec3 color = distance * (
        reflectivity * sky + (1 - reflectivity) * upwelling
    ) + (1 - distance) * air;

    // no foam just yet

    glFragColor = vec4(color, 0.5);
}