// VERTEX SHADER
#version 330 core

#define WAVES_NUMBER 90
#define MAX_AMPLITUDE 0.9
#define MAX_SPEED 0.7
#define WIND_SPEED 0.7
#define choppy_coef 0.38

    // fetch
#define F 300
#define G 9.81



const float U_10 = G / 1.17; 
const float w_p = pow(22 * (G * G / U_10 / F), 0.33);
const float alpha = 0.076 * pow(U_10 * U_10 / F / G, 0.22);  

#define PI 3.14159265359

const vec2 WIN_DIR = vec2(0.34202014,0.93969262);
const float wind_speed = 10;

float L = wind_speed * wind_speed / G;
const vec2 array_of_dirs[200] = vec2[200](
    vec2(-0.9703, -0.2421),
    vec2(-0.3117, 0.9502),
    vec2(0.9743, -0.2253),
    vec2(-0.3973, 0.9177),
    vec2(-0.3462, -0.9382),
    vec2(0.0189, 0.9998),
    vec2(-0.4160, 0.9094),
    vec2(-0.9948, 0.1020),
    vec2(0.2230, 0.9748),
    vec2(-0.8702, -0.4927),
    vec2(0.8069, 0.5906),
    vec2(-0.9090, -0.4167),
    vec2(0.3259, 0.9454),
    vec2(-0.9602, -0.2792),
    vec2(-0.9934, -0.1145),
    vec2(0.9443, 0.3291),
    vec2(-0.9316, -0.3635),
    vec2(0.3923, 0.9198),
    vec2(-0.0500, -0.9988),
    vec2(0.3605, -0.9328),
    vec2(0.1137, 0.9935),
    vec2(1.0000, -0.0040),
    vec2(0.7959, 0.6054),
    vec2(-0.9999, 0.0131),
    vec2(0.9983, 0.0588),
    vec2(0.6051, -0.7962),
    vec2(0.5294, -0.8484),
    vec2(-0.0423, 0.9991),
    vec2(0.9814, 0.1918),
    vec2(-0.1480, -0.9890),
    vec2(0.3914, -0.9202),
    vec2(0.6286, 0.7777),
    vec2(-0.8722, 0.4892),
    vec2(-0.8293, -0.5588),
    vec2(-0.3610, 0.9325),
    vec2(-0.6284, -0.7779),
    vec2(-0.9138, -0.4061),
    vec2(0.3059, 0.9521),
    vec2(-0.9988, 0.0490),
    vec2(-0.3463, -0.9381),
    vec2(-0.8238, 0.5669),
    vec2(0.9960, 0.0888),
    vec2(0.9872, -0.1597),
    vec2(-0.8979, 0.4402),
    vec2(-0.1143, -0.9934),
    vec2(-0.2828, -0.9592),
    vec2(0.9665, 0.2565),
    vec2(-0.8562, 0.5167),
    vec2(-0.4510, 0.8925),
    vec2(-0.9753, -0.2209),
    vec2(-0.8097, -0.5869),
    vec2(0.1570, 0.9876),
    vec2(0.3153, -0.9490),
    vec2(0.6378, -0.7702),
    vec2(-0.9855, -0.1696),
    vec2(0.8050, 0.5933),
    vec2(0.3860, 0.9225),
    vec2(0.5503, -0.8350),
    vec2(0.9998, -0.0177),
    vec2(0.8836, -0.4683),
    vec2(0.7262, -0.6875),
    vec2(0.8128, -0.5825),
    vec2(-0.3562, 0.9344),
    vec2(-0.2017, 0.9795),
    vec2(-0.4025, 0.9154),
    vec2(-0.9425, 0.3342),
    vec2(-0.4603, -0.8878),
    vec2(-0.0090, -1.0000),
    vec2(-0.9959, -0.0905),
    vec2(-0.0647, 0.9979),
    vec2(-0.8651, -0.5016),
    vec2(-0.0704, -0.9975),
    vec2(0.8362, -0.5485),
    vec2(-0.9937, -0.1119),
    vec2(0.2283, -0.9736),
    vec2(0.5996, 0.8003),
    vec2(0.6643, 0.7475),
    vec2(0.3428, 0.9394),
    vec2(0.1391, 0.9903),
    vec2(0.3196, 0.9475),
    vec2(0.6766, -0.7364),
    vec2(0.0370, 0.9993),
    vec2(-0.9526, -0.3043),
    vec2(0.9164, -0.4003),
    vec2(0.6535, -0.7570),
    vec2(-0.7378, -0.6750),
    vec2(0.6119, 0.7909),
    vec2(-0.3595, -0.9332),
    vec2(0.1347, -0.9909),
    vec2(-0.4406, -0.8977),
    vec2(-0.8987, -0.4386),
    vec2(0.8482, 0.5297),
    vec2(0.9330, 0.3598),
    vec2(0.1424, 0.9898),
    vec2(-0.9012, -0.4334),
    vec2(-0.4945, -0.8692),
    vec2(0.8089, 0.5880),
    vec2(0.9996, 0.0268),
    vec2(0.9943, -0.1065),
    vec2(-0.9995, 0.0314),
    vec2(-0.9997, -0.0227),
    vec2(0.9110, -0.4125),
    vec2(0.9608, 0.2773),
    vec2(-0.9754, -0.2206),
    vec2(-0.8370, -0.5471),
    vec2(0.0322, 0.9995),
    vec2(0.5155, 0.8569),
    vec2(-0.2506, 0.9681),
    vec2(0.9047, 0.4261),
    vec2(0.1393, -0.9902),
    vec2(-0.9882, 0.1534),
    vec2(-0.7169, -0.6972),
    vec2(-0.7212, 0.6928),
    vec2(0.1746, -0.9846),
    vec2(-0.9571, 0.2899),
    vec2(0.7885, 0.6151),
    vec2(-0.4874, -0.8732),
    vec2(0.9941, 0.1087),
    vec2(0.9997, -0.0239),
    vec2(-0.9154, 0.4025),
    vec2(0.1946, -0.9809),
    vec2(-0.8959, -0.4442),
    vec2(-0.0757, 0.9971),
    vec2(0.3728, -0.9279),
    vec2(-0.2250, -0.9744),
    vec2(0.3660, -0.9306),
    vec2(-0.0906, 0.9959),
    vec2(-0.0940, -0.9956),
    vec2(-0.9883, 0.1525),
    vec2(-0.9758, -0.2185),
    vec2(0.7264, -0.6872),
    vec2(-0.4829, 0.8757),
    vec2(0.5002, 0.8659),
    vec2(-0.6603, -0.7510),
    vec2(-0.9954, -0.0958),
    vec2(-0.1504, -0.9886),
    vec2(0.3805, -0.9248),
    vec2(-0.1958, 0.9806),
    vec2(0.9600, 0.2799),
    vec2(-0.0064, 1.0000),
    vec2(0.9967, -0.0816),
    vec2(0.9736, 0.2285),
    vec2(0.7336, -0.6796),
    vec2(-0.2659, 0.9640),
    vec2(0.5134, -0.8581),
    vec2(0.5744, 0.8186),
    vec2(-0.2002, 0.9797),
    vec2(0.5996, 0.8003),
    vec2(0.3005, 0.9538),
    vec2(-0.9415, -0.3371),
    vec2(0.7927, 0.6096),
    vec2(-0.3865, 0.9223),
    vec2(0.4336, -0.9011),
    vec2(0.0804, -0.9968),
    vec2(-0.3503, 0.9366),
    vec2(0.9080, 0.4190),
    vec2(0.9999, -0.0159),
    vec2(-1.0000, -0.0051),
    vec2(-0.9206, 0.3905),
    vec2(0.9999, -0.0125),
    vec2(-0.4467, 0.8947),
    vec2(0.9779, 0.2092),
    vec2(0.4323, -0.9017),
    vec2(0.4420, 0.8970),
    vec2(0.9971, 0.0761),
    vec2(0.1861, 0.9825),
    vec2(0.9546, -0.2980),
    vec2(0.5401, -0.8416),
    vec2(0.9950, -0.0995),
    vec2(0.9419, -0.3359),
    vec2(0.9615, -0.2748),
    vec2(0.5882, 0.8087),
    vec2(-0.6655, -0.7464),
    vec2(-0.3983, 0.9172),
    vec2(-0.8824, 0.4705),
    vec2(-0.5385, -0.8426),
    vec2(0.9937, -0.1122),
    vec2(-0.8402, 0.5422),
    vec2(-0.5693, 0.8221),
    vec2(0.9966, -0.0828),
    vec2(0.8870, -0.4618),
    vec2(0.7539, 0.6570),
    vec2(0.4403, -0.8978),
    vec2(0.6931, 0.7208),
    vec2(0.9250, -0.3799),
    vec2(-0.1214, 0.9926),
    vec2(-0.1217, 0.9926),
    vec2(0.3801, 0.9250),
    vec2(-0.5712, 0.8208),
    vec2(-0.2334, 0.9724),
    vec2(0.7195, -0.6945),
    vec2(-0.8802, -0.4745),
    vec2(-0.9700, 0.2433),
    vec2(0.1184, 0.9930),
    vec2(0.3426, -0.9395),
    vec2(-0.6764, -0.7365),
    vec2(-0.7831, 0.6219),
    vec2(-0.9347, -0.3555),
    vec2(0.9915, 0.1303),
    vec2(0.7318, 0.6815)
);
layout (location = 0) in vec3 in_Position;

out vec3 position;
out vec3 normal;
out vec3 unnormalized_normal;
out float max_amplitude;

uniform mat4 perspective_mat;
uniform float time;


void main()
{   

    
    float u = in_Position.x;
    float v = in_Position.z;
    u = in_Position.x / WAVES_NUMBER;
    v = in_Position.z / WAVES_NUMBER;
    
    // float dx = MAX_AMPLITUDE / WAVES_NUMBER; // for iteration
    float A = MAX_AMPLITUDE;
    float w; 
    float s; 
    vec2 dir;
    

    vec3 paramatric_position = vec3(0, 0, 0);
    normal = vec3(0);

        // accumulate sum of trigonometric entities (position)
    float x = -2.0 * MAX_AMPLITUDE; 
    const float dx = (2.0 * MAX_AMPLITUDE - (-2.0 * MAX_AMPLITUDE)) / WAVES_NUMBER;

        // for guassian sampling machine
    float k;
    float k_4;
    float philips;
    float dot_wk;

    for (int i = 0; i < WAVES_NUMBER; i++)   // ★ fixed bounds
    {
        dir = array_of_dirs[i];

        // centered Gaussian sampling
        x = float(i) * dx - 2.0 * MAX_AMPLITUDE;

        // wavelength λ (was incorrectly treated as k before)
        float lambda = MAX_AMPLITUDE * exp(-(x * x) / (MAX_AMPLITUDE * MAX_AMPLITUDE));
        lambda = max(lambda, 0.001);

        // wave number k = 2π / λ
        k = 2.0 * PI / lambda;
        k_4 = k * k * k * k;

        // angular frequency (deep water dispersion)
        w = sqrt(G * k);
        w = pow(w, 2.25);

        // speed (phase speed, keeping your assumption)
        s = w * 0.035 * MAX_SPEED;

        // Phillips spectrum (correct k usage + stability)
            dot_wk = max(dot(normalize(WIN_DIR), dir), 0.0);
        // dot_wk = dot(normalize(WIN_DIR), dir), 0.0;

        philips =
            WIND_SPEED *
            exp(-1.0 / (k * k * L * L)) /
            k_4 * 
            (pow(dot_wk, 1.5));
            // (dot_wk * dot_wk * dot_wk * dot_wk * dot_wk);
            // (dot_wk * dot_wk * dot_wk * dot_wk);
            // (dot_wk * dot_wk);
            // dot_wk;
            // 1;
        A = sqrt(max(philips, 0.0));
        A = pow(A, 0.6);
        // A *= WAVES_NUMBER;

            // trigonometric coef
        float p = w * (u * dir.x + v * dir.y) + s * time;

        float Dz_coef = A * w * cos(p);
        vec2 Dz = Dz_coef * dir;
        
        float displacement = choppy_coef * dot(Dz, dir);
        float computed_cos = cos(p + displacement);
        float computed_sin = sin(p);

        paramatric_position += vec3(
            u + ((dir.x / w) * (displacement * computed_cos)),
            (A * computed_sin),
            v + ((dir.y / w) * (displacement * computed_cos))
        );

        normal += vec3(
            -dir.x * A * w * cos(p),
            (1.0 + choppy_coef * A * w * computed_sin - sin(p + choppy_coef * Dz_coef) * (1 - choppy_coef * A * w * computed_sin)),
            -dir.y * A * w * cos(p)
        );
    }
    unnormalized_normal = normal;
    normal = normalize(normal);
    

    gl_Position = perspective_mat * vec4(paramatric_position, 1.0);
    position = paramatric_position;
    max_amplitude = MAX_AMPLITUDE;
}

// FRAGMENT SHADER


#version 330 core

const vec3 LIGHT_COLOR = vec3(0.95, 0.94, 0.87);

in vec3 normal;
in vec3 position;
in float max_amplitude;
in vec3 unnormalized_normal;
uniform vec3 water_color;
uniform vec3 light_dir; // this is actually light_pos, im lazy to change the name
uniform vec3 cam_pos;
uniform vec3 orientation;
uniform vec3 sky_color;

out vec4 glFragColor;

void main()
{   
    vec3 lightDir = normalize(light_dir - cam_pos);    

        // fresnel
    float reflectivity = 1;
    
    vec3 eye_dir = normalize(cam_pos - position); 


    // float incident_rad = acos(abs(dot(normal, -light_dir)));
    // float incident_rad = acos(dot(normal, -eye_dir));
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

        // now we got the ambient: ambient = reflectivity * SKY_COLOR + transmissivity * WATER_COLOR (idk)
    reflectivity  = 0.5 * (a * a + b * b);
    float transmissivity = 1 - reflectivity;




    // doing plastic shader first
    vec3 baseColor = (water_color * transmissivity + sky_color * reflectivity);
        // ambient color
    float ambient_strength = 0.9;
    vec3 ambient = ambient_strength * baseColor;

        // diffuse
    float diffuse_strength = 0.10;
    float diffuse_lit = max(0, dot(-lightDir, normal));
    vec3 diffuse = diffuse_strength * diffuse_lit * sky_color;
    
        // specular
    float specular_strength = 1.9;
    float specular_lit = dot(reflect(lightDir, normal), normalize(cam_pos - position));
    specular_lit = max(0, specular_lit);
    vec3 specular = specular_strength * pow(specular_lit, 90) * sky_color;

    
    float foam_maker = pow(
                max(
                    0, 
                    dot(normal, vec3(0,1,0))
                )
        , 10)
        // ;
            * pow((position.y + max_amplitude / 2) / (2 * max_amplitude / 2), 5);
    // foam_maker = pow(foam_maker, 10);
    // foam_maker = max(foam_maker, 0);
    // foam_maker = max(foam_maker, 0.0) * 0.00;
    // foam_maker = max(foam_maker, 0.0) * 0.00;
        

    glFragColor = vec4((ambient + diffuse + specular), 0.1);
    // glFragColor += vec4(vec3(
    //     pow(dot(normal, vec3(0, 1, 0)), 50)
    //     ), 1.0);
    // glFragColor.xyz = baseColor;
    glFragColor += vec4(vec3(
        pow((clamp((length(unnormalized_normal) - 120) / 60, 0, 1)), 2.3)
        ), 1) * 1.8;
    
    // glFragColor.xyz += foam_maker * sky_color;
}

