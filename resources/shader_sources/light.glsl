// VERTEX SHADER
#version 330 core
layout(location = 0) in vec3 localPosition;
layout(location = 1) in vec2 TexCoord;
layout(location = 2) in vec3 localNormal;

uniform mat4 Camera_Projection;
uniform mat4 Translation_Mat;
uniform mat4 Scale_Mat;

out vec3 worldPosition;


void main()
{
    worldPosition = (Translation_Mat * Scale_Mat * vec4(localPosition, 1.0)).xyz;

    gl_Position = Camera_Projection * vec4(worldPosition, 1.0);
}
// FRAGMENT SHADER
#version 330 core

out vec4 glFragColor;

void main()
{
    glFragColor = vec4(1.0, 1.0, 1.0, 1.0);
}