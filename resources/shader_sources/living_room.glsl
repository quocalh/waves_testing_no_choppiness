// VERTEX SHADER
#version 330 core

layout(location = 0) in vec3 localPosition;
layout(location = 1) in vec2 texCoord;
layout(location = 2) in vec3 localNormal;

out vec3 worldNormal;
out vec3 worldPosition;
out vec2 TexCoord;
out float depth;

uniform mat4 Camera_Projection;

uniform mat4 Translation_Mat;
uniform mat4 Rotation_Mat;
uniform mat4 Scale_Mat;


void main()
{   
    worldPosition = (Translation_Mat * Rotation_Mat * Scale_Mat * vec4(localPosition, 1.0)).xyz;
    worldNormal = (Rotation_Mat * vec4(localNormal, 1.0)).xyz;
    TexCoord = texCoord;
    
    vec4 ProjectionPoint = Camera_Projection * vec4(worldPosition, 1.0);
    depth = ProjectionPoint.w / 10;
    gl_Position = ProjectionPoint;
}

// FRAGMENT SHADER
#version 330 core

in vec2 TexCoord;
in vec3 worldNormal;
in vec3 worldPosition;
in float depth;

out vec4 glFragColor;

uniform vec3 view_pos;

uniform vec3 Ka; 
uniform vec3 Kd;
uniform float Ns;
uniform vec3 Ks;

uniform vec3 RandomColor;
uniform vec3 LightSource;

#define MAX_LIGHT_SOURCES 100
vec3 light_sources[MAX_LIGHT_SOURCES];

void main()
{   
    // will soon be a loop
    light_sources[0] = LightSource;
    // light_sources[0] = view_pos;
    vec3 light_dir = light_sources[0] - worldPosition;
    light_dir = light_dir / length(light_dir);
    

    float AmbientStrength = 0.1;
    vec3 AmbientColor = AmbientStrength * Ka;

    float DiffuseStrength = 1.0;
    vec3 DiffuseColor = DiffuseStrength * max(0, dot(light_dir, worldNormal)) * Kd;

    float SpecularStrength = 1;
    
    
    vec3 reflectDir = reflect((worldPosition - view_pos) / length(worldPosition - view_pos), worldNormal);
    vec3 SpecularColor = SpecularStrength 
                            * pow(max(dot(reflectDir, light_dir), 0), Ns) 
                            * Ks;

    glFragColor = vec4(AmbientColor * RandomColor, 1.0);
    glFragColor+= vec4(DiffuseColor * RandomColor, 1.0);
    glFragColor+= vec4(SpecularColor * RandomColor, 1.0);
    // glFragColor = vec4(vec3(depth), 1.0);
    // glFragColor = vec4(vec3(1) * RandomColor, 1.0);
}