import numpy as np
from OpenGL.GL import *

import time as t

import pygame as pg
from pygame.locals import *

import ctypes

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(__file__) + "/..")



from components.vbo import VBO
from components.vao import VAO, AttributeLayout, Layout
from components.ibo import IBO
from components.settings import *
from components.shaders import  Shader, ShaderProgram
from components.texture import Texture2D

# create the context first
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)

# shaders
vertex_shader_src = """
#version 330 core

layout(location = 0) in vec2 lPos;
layout(location = 1) in vec3 Color;
layout(location = 2) in vec2 TexCoord;

out vec2 aPos;
out vec3 aColor;
out vec2 texCoord;

void main()
{
    gl_Position = vec4(lPos, 0.0, 1.0);
    aPos = lPos;
    aColor = Color;
    texCoord = TexCoord;
}
"""
vertex_shader = Shader(GL_VERTEX_SHADER, vertex_shader_src)

fragment_shader_src = """
#version 330 core

in vec2 aPos;
in vec3 aColor;
in vec2 texCoord;

out vec4 glFragColor;

uniform vec3 subtrahend;
uniform int subtrahend_mult;

uniform vec3 array[1000];

uniform sampler2D texture_1;
uniform sampler2D texture_4;

void main()
{   
    vec4 texture_ah = texture(texture_1, texCoord);
    vec4 texture_aha = texture(texture_4, texCoord);

    glFragColor = vec4(aColor, 1.0);  
    glFragColor += texture_ah / 2.0;  
    glFragColor += texture_aha / 2.0;  
    glFragColor -= vec4(subtrahend, 0.0) * subtrahend_mult;

    glFragColor.xyz += array[0];
    glFragColor.xyz += array[1];
    glFragColor.xyz += array[2];
}   

"""
fragment_shader = Shader(GL_FRAGMENT_SHADER, fragment_shader_src)

shader_program = ShaderProgram(vertex_shader, fragment_shader)
shader_program.LinkingShaders()


# VAO, VBO, IBO

vertices = np.array([
    [-0.5,  0.5, 1.0, 1.0, 1.0, 0.0, 1.0],
    [ 0.5,  0.5, 1.0, 0.0, 0.0, 1.0, 1.0],
    [ 0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 0.0],
    [-0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 0.0],
], dtype = np.float32)
attrib_layout = AttributeLayout([
    Layout(2, np.float32), # position
    Layout(3, np.float32), # color
    Layout(2, np.float32), # texcord
])


"""
vertices = np.array([
    [-0.5, 0.5, 1.0, 1.0, 1.0,],
    [0.5, 0.5, 1.0, 0.0, 0.0,],
    [0.5, -0.5, 0.0, 1.0, 0.0,],
    [-0.5, -0.5, 0.0, 0.0, 1.0,],
], dtype = np.float32)
attrib_layout = AttributeLayout([
    Layout(2, np.float32), 
    Layout(3, np.float32),
])
"""


indices = np.array([
    # 0, 1, 2, 3
    0, 1, 2,
    0, 2, 3,
], dtype = np.uint32)


# VAO, VBO, IBO
vao = VAO(attrib_layout)
vao.Bind()

vbo = VBO()
vbo.Bind(GL_ARRAY_BUFFER)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

ibo = IBO()
ibo.Bind(GL_ELEMENT_ARRAY_BUFFER)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

vao.SetUpVertexArray()

vao.Unbind()
vbo.Unbind()



# texture
wood_tex = Texture2D(r"C:\Users\admin\Downloads\container2.png")
wood_tex.Construct()

martial_tex = Texture2D(r"C:\Users\admin\Downloads\Screenshot 2025-11-17 071353.png")
martial_tex.Construct()

# set uniform id for textures

max_texture_image_units =glGetIntegerv(GL_MAX_TEXTURE_IMAGE_UNITS)
print(f"hello gang, there are {max_texture_image_units} available for uses")

texture_1 = glGetUniformLocation(shader_program._ref, "texture_1")
if texture_1 == -1: print(f"not found")

texture_4 = glGetUniformLocation(shader_program._ref, "texture_4")
if texture_4 == -1: 
    print(f"not found"); print("wh")

color_subtrahend = np.array([0.1, 0.1, 0.1], dtype = np.float32)
color_subtrahend_location = glGetUniformLocation(shader_program._ref, "subtrahend")
if color_subtrahend_location == -1:
    print("subtrahend not found")

color_subtrahend_mult = np.int32(5)
color_subtrahend_mult_location = glGetUniformLocation(shader_program._ref, "subtrahend_mult")
if color_subtrahend_mult_location == -1:
    print("subtrahend not found")

array = np.array([
    [0.4, 0, 0], [0, 0.4, 0], [1, 1, 0.4], [1, 1, 0],
], dtype = np.float32)
array_location = glGetUniformLocation(shader_program._ref, "array")
if array_location == -1:
    print("array not found")



print(color_subtrahend_location)
print(texture_1)
print(texture_4)

shader_program.Use()
glUniform1i(texture_1, 1)
glUniform1i(texture_4, 4)
shader_program.Unuse()

running = True
clock = pg.time.Clock()

prevTime = t.time()

while running:
    glClearColor(0.1, 0.2, 0.3, 1)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    shader_program.Use()
    vao.Bind()
    
    glActiveTexture(GL_TEXTURE4)
    martial_tex.Bind(GL_TEXTURE_2D)

    # glActiveTexture(GL_TEXTURE0)

    glActiveTexture(GL_TEXTURE1)
    wood_tex.Bind(GL_TEXTURE_2D)

    # uniform

        # subtrahend
    glUniform3f(color_subtrahend_location, color_subtrahend[0], color_subtrahend[1], color_subtrahend[2])
        # subtrahend mult
    glUniform1i(color_subtrahend_mult_location, color_subtrahend_mult)

    glUniform3fv(array_location, 3, array)


    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, ctypes.c_void_p(0))

    shader_program.Unuse()

    pg.display.flip()
    pg.display.set_caption(f"{clock.get_fps() // 1}")
    clock.tick(0)

pg.quit()

"""

IN CONCLUSION

FOR TEXTURES, THE CONNECTION ACTS LIKE A HANDSHAKE PROTOCOL
{
    IF THE SHADER DEMANDS IT BUT THERE IS NO PROVIDER IN THE CPU -> RETURN VEC4(0);
        E.G.
            MAIN.PY:
                LOCATION = GLGETGETUNIFORMLOCATION(SHADER_PROGRAM_REF, "TEXTURE_1_") # INTENTIONAL TYPO
                GLUNIIFORM1I(LOCATION, <TEXTURE_SLOT_ID>)

                IN THE LOOP:
                    GLACTIVETEXTURE(GL_TEXTURE0 + <TEXTURE_SLOT_ID>)
                    <DESIRED_TEXTURE>.BIND(GL_TEXTURE_2D)
            SHADERS:
                UNIFORM SAMPLER2D TEXTURE_1;
                -> TEXTURE(TEXTURE_1, TEXCOORD) RETURNS VEC4(0)
            
    IF THE PROVIDER DELIVER IT BUT THERE IS NO DEMANDS (EITHER LOCATION = -1 OR THE SHADER DID NOT DEFINE THE GONG-INTO ADDRESS) -> RETURN VEC4(0);
        E.G.
            MAIN.PY:
                
                IN THE LOOP:
                LOCATION = GLGETGETUNIFORMLOCATION(SHADER_PROGRAM_REF, "TEXTURE_1")
                GLUNIIFORM1I(LOCATION, <TEXTURE_SLOT_ID>)

                IN THE LOOP:
                    GLACTIVETEXTURE(GL_TEXTURE0 + <TEXTURE_SLOT_ID>)
                    <DESIRED_TEXTURE>.BIND(GL_TEXTURE_2D)
                
            SHADER:
                // MEWING, INTENTIONALLY USING THE WRONG NAME
                UNIFORM SAMPLER2D TEXTURE_1_;
                -> TEXTURE(TEXTURE_1_, TEXCOORD) -> VEC4(0);

    I KNOW BOTH CASES SHOW THE SAME THING, LITERALLY, BUT I JUST WANT YOU TO SEE THE COONNECTION THAT I'M TALKING ABOUT


    FOR ORDINARY VARIABLES, IT STILL HOLDS
        IF THE PROVIDER FAILED TO PROVIDE THE DESIRED VALUE:
            FOR A (GLUNIFORM3F -> VEC3())
                IT RETURNS A VEC3(0); 
            FOR A (GLUNIFORM1I -> INT())
                IT RETURNS AN INT OF 0;

    FOR ARRAY VALUES (E.G. UNIFORM VEC3 ARRAY[1000])
        TO MAKE IT LIKE A VECTOR (OR A PYTHONIC LIST) 
            MAKE SURE TO CREATE AN INT UNIFORM STATING THE CURRENT ELEMENT IN THE LIST
                -> THE ONLY CONSTRAINT IS THAT THE LIST ONLY HAS 1000 ELEMENT MAX (WE SET ARRAY[1000])
        THE COUNT DEFINED IN THE UNIFORM FUNCTION IS IMPORTANT
            IT TELLS HOW MUCH VALUE IS GOING  IN
                GIVE A LIST OF 50 VEC3
                    -> COUNT = 20 -> ONLY REGISTER THE FIRST 20 ONES
                    -> COUNT = 60 -> THE 10 LAST BECOME VEC3(0)
                ERM ACTUALLY (UNIFORM VEC3 ARRAY[1000]) THIS MEANS CREATE 1000 VEC3(0)
                    OUR JOB IS JUST USE IT TO STORE VALUES, THAT'S IT
                    

}

"""