import pygame as pg
import numpy as np
import numba as nb
import os, sys
import time
import ctypes


if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__) + "/..")

from abstraction.camera import *
from abstraction.wavefront import *
from abstraction.custom import fuvector, fvector, vector, GetRotationMat4
from abstraction.shader_parsing import *

from components.vao import *
from components.vbo import *
from components.ibo import *
from components.shaders import *
from components.settings import *
from components.uniform_package import *
 

    # Creating vertices
X_NUM = 1000
Y_NUM = 1000
X_UNIT = 0.1
Y_UNIT = 0.1
WATER_COLOR = np.array([0.0, 0.2, 0.4], dtype = np.float32)
WATER_COLOR = fvector(61,93,126) / 255
WATER_COLOR = fvector(0,30,59) / 255
# WATER_COLOR = np.array([0.7, 0.7, 0.7], dtype = np.float32)

# SKY_COLOR = fvector(0.3843, 0.7569, 0.8980)
SKY_COLOR = fvector(0.6275, 0.8510, 0.9373)
SKY_COLOR = fvector(0.8118, 0.9255, 0.9686)
SKY_COLOR = fvector(207,236,247) / 255


# SKY_COLOR = fvector(0.53, 0.81, 0.98)

vertices = np.zeros((X_NUM * Y_NUM, 3), dtype = np.float32)

    # creating a 1d array of points with (i % COL_NUM, i // COL_NUM)
for i in range(X_NUM * Y_NUM):
    vertices[i][0] = i % X_NUM * X_UNIT
    vertices[i][2] = i // X_NUM * Y_UNIT

    # indices // for triangle strips
indices = np.zeros((
    ((X_NUM - 1) *  (Y_NUM - 1) * 6 * 4),
), dtype = np.int32)

for i in range(X_NUM - 1):
    for j in range(Y_NUM - 1):
            # 123 134
        
            # first triangle    
        indices[(i +  j * X_NUM) * 6 + 0] = (i) + (j) * X_NUM         # (i, j) + (0, 0)
        indices[(i +  j * X_NUM) * 6 + 1] = (i) + (j + 1) * X_NUM     # (i, j) + (0, 1)
        indices[(i +  j * X_NUM) * 6 + 2] = (i + 1) + (j + 1) * X_NUM # (i, j) + (1, 1)

            # second triangle
        indices[(i +  j * X_NUM) * 6 + 3] = (i) + (j) * X_NUM         # (i, j) + (0, 0)
        indices[(i +  j * X_NUM) * 6 + 4] = (i + 1) + (j + 1) * X_NUM # (i, j) + (1, 1)
        indices[(i +  j * X_NUM) * 6 + 5] = (i + 1) + (j) * X_NUM     # (i, j) + (1, 0)
        


camera = Camera(sensitivity = 0.5, far = 1050)
camera._velocity *= 1.5

running = True
screen = pg.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
clock = pg.time.Clock()

glEnable(GL_DEPTH_TEST)

vertex_shader_src, fragment_shader_src = ReadShaderFile(r"resources\shader_sources\waves_typical.glsl")
shader_prog = TestingShaderProgram(
    vertex_shader = Shader(GL_VERTEX_SHADER, vertex_shader_src),
    fragment_shader = Shader(GL_FRAGMENT_SHADER, fragment_shader_src),
    uniform_names_set = [
        "perspective_mat",
        "time",
        "water_color",  

        "light_dir",
        "cam_pos",
        "orientation",
        "sky_color",
    ]
)



shader_prog.Use()
# glUniform3f(shader_prog._uniform_location["water_color"], *WATER_COLOR)
glUniform3f(shader_prog.UserGetUniformLocation("water_color"), *WATER_COLOR)
glUniform3f(shader_prog._uniform_location["sky_color"], *SKY_COLOR)
shader_prog.Unuse()

uniform_location: dict = shader_prog._uniform_location

mesh = Mesh()
mesh._vertices = vertices
mesh._indices = indices
mesh._attrib_layout = AttributeLayout([Layout(3, dtype = np.float32),])
mesh.OpenGLConstruct()

TOGGLE_CHANGE_SHADER = True
TOGGLE_TIME_STOP = False

t = 0
prevTime = time.time()
while running:
    
    dt = time.time() - prevTime
    prevTime = time.time()

    for event in pg.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                running = False

            if event.key == K_q:
                TOGGLE_IS_WIREFRAME_MODE = not TOGGLE_IS_WIREFRAME_MODE
                if TOGGLE_IS_WIREFRAME_MODE:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                else:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            
            if event.key == K_r:
                TOGGLE_CHANGE_SHADER = not TOGGLE_CHANGE_SHADER

            if event.key == K_f:
                TOGGLE_TIME_STOP = not TOGGLE_TIME_STOP

    camera.KeyInput(dt)
    camera.MouseInput(dt)
    
    dt = 0 if TOGGLE_TIME_STOP else dt
    t += dt


    glClearColor(*SKY_COLOR, 1)
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

    shader = shader_prog
    shader.Use()
        # binding variables
            # vertex shader
    glUniform1f(shader._uniform_location["time"], t)
    glUniformMatrix4fv(shader._uniform_location["perspective_mat"], 1, GL_TRUE, camera.GetTransformationMat)
            # fragment shader
    glUniform3f(shader._uniform_location["light_dir"], *fvector(8, 5, 1))
    glUniform3f(shader._uniform_location["cam_pos"], *camera._pos)
    glUniform3f(shader._uniform_location["orientation"], *camera._orientation)


    mesh._vao.Bind()
    glDrawElements(GL_TRIANGLES, len(mesh._indices), GL_UNSIGNED_INT, ctypes.c_void_p(0))
 
    clock.tick(200)
    pg.display.flip()
    pg.display.set_caption(f"FPS: {clock.get_fps() // 1}")

shader_prog.Unuse()
shader_prog.Delete()

    

