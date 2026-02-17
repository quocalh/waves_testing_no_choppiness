import numpy as np



colors = np.array([
    [0.000, 0.000, 0.000],  # black
    [1.000, 1.000, 1.000],  # white
    [1.000, 0.000, 0.000],  # red
    [0.000, 1.000, 0.000],  # green
    [0.000, 0.000, 1.000],  # blue
    [1.000, 1.000, 0.000],  # yellow
    [1.000, 0.000, 1.000],  # magenta
    [0.000, 1.000, 1.000],  # cyan
    [0.500, 0.500, 0.500],  # gray
    [0.750, 0.750, 0.750],
    [0.250, 0.250, 0.250],
    [0.800, 0.200, 0.200],
    [0.200, 0.800, 0.200],
    [0.200, 0.200, 0.800],
    [0.900, 0.600, 0.100],
    [0.600, 0.100, 0.900],
    [0.100, 0.900, 0.600],
    [0.400, 0.200, 0.600],
    [0.600, 0.400, 0.200],
    [0.200, 0.600, 0.400],
    [0.900, 0.300, 0.300],
    [0.300, 0.900, 0.300],
    [0.300, 0.300, 0.900],
    [0.900, 0.900, 0.300],
    [0.900, 0.300, 0.900],
    [0.300, 0.900, 0.900],
    [0.650, 0.350, 0.150],
    [0.350, 0.650, 0.150],
    [0.150, 0.350, 0.650],
    [0.850, 0.550, 0.250],
    [0.250, 0.850, 0.550],
    [0.550, 0.250, 0.850],
    [0.700, 0.100, 0.100],
    [0.100, 0.700, 0.100],
    [0.100, 0.100, 0.700],
    [0.700, 0.700, 0.100],
    [0.700, 0.100, 0.700],
    [0.100, 0.700, 0.700],
    [0.950, 0.500, 0.500],
    [0.500, 0.950, 0.500],
    [0.500, 0.500, 0.950],
    [0.950, 0.950, 0.500],
    [0.950, 0.500, 0.950],
    [0.500, 0.950, 0.950],
    [0.300, 0.150, 0.050],
    [0.150, 0.300, 0.050],
    [0.050, 0.150, 0.300],
    [0.850, 0.850, 0.850],
    [0.100, 0.100, 0.100],
], dtype = np.float32)


if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.dirname(__file__) + "/..")



from meshes.material import MaterialManager, MATERIAL_SLOT, TEXTURE_SLOT

from meshes.mesh import MeshManager, Mesh



from pygame.locals import *
import pygame as pg
from OpenGL.GL import *
import ctypes



from components.vbo import *
from components.vao import *
from components.ibo import *
from components.shaders import *
from abstraction.camera import *

from abstraction.shader_parsing import *
from abstraction.custom import fvector, fuvector, GetRotationMat4
from components.uniform_package import *

screen = pg.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
clock = pg.time.Clock()
import time
camera = Camera(sensitivity = 0.5)


light_vertex_shader_src, fragment_light_shader_src = ReadShaderFile(r"resources\shader_sources\light.glsl")
light_shader_prog = TestingShaderProgram(
    Shader(GL_VERTEX_SHADER, light_vertex_shader_src),
    Shader(GL_FRAGMENT_SHADER, fragment_light_shader_src),
    (
        "Camera_Projection",
        "Translation_Mat",
        "Scale_Mat",
    )
)
light_mesh_manager = MeshManager(MaterialManager())
light_mesh_manager.ReadBothMaterialAndObjectFile(
    material_directory = r"resources\obj_files\obj\cube\cube.mtl",
    object_directory = r"resources\obj_files\obj\cube\cube.obj"
)
for mesh_name in light_mesh_manager._dict_name_mesh:
    mesh: Mesh = light_mesh_manager._dict_name_mesh[mesh_name]
    mesh.OpenGL_contruct()
cube: Mesh = light_mesh_manager._dict_name_mesh["Cube"]
cube._pos = fvector(2.0, 2.0, 0.0)
cube._scale = 0.1

vertex_shader_src, fragment_shader_src = ReadShaderFile(r"resources\shader_sources\living_room.glsl")
vertex_shader = Shader(GL_VERTEX_SHADER,  vertex_shader_src)
frag_shader = Shader(GL_FRAGMENT_SHADER, fragment_shader_src)
shader_prog = TestingShaderProgram(vertex_shader, frag_shader, (
    # VERTEX SHADER
    "Camera_Projection", 
    "Translation_Mat",
    "Rotation_Mat",
    "Scale_Mat",
    # FRAGMENT SHADER   
    "view_pos",
    "Ka",
    "Kd",
    "Ns",
    "Ks",
    "RandomColor",
    "LightSource",
))

mesh_manager = MeshManager(MaterialManager())
mesh_manager.ReadMaterialFile(
    r"resources\obj_files\obj\20-livingroom_obj\InteriorTest.mtl"
)
mesh_manager.ReadObjectFile(
    r"resources\obj_files\obj\20-livingroom_obj\InteriorTest.obj"
)
for mesh_name in mesh_manager._dict_name_mesh:
    mesh: Mesh = mesh_manager._dict_name_mesh[mesh_name]
    mesh.OpenGL_contruct()

print(f"niche: {len(mesh_manager._dict_name_mesh)}")

running = True
# running = False

t = 0.0
prevTime = time.time()
glEnable(GL_DEPTH_TEST)
while running:

    dt = time.time() - prevTime
    prevTime = time.time()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.1, 0.2, 0.3, 1)

    camera.KeyInput(dt)
    camera.MouseInput(dt)

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
            if event.key == K_e:
                TOGGLE_TIME_STOP = not TOGGLE_TIME_STOP
                
    dt = TOGGLE_TIME_STOP * dt
    t += dt

    # cube._pos[0] = 1 + np.cos(t)
    # cube._pos[2] = -1.5 + 3 * np.sin(t)
    # print(cube._pos)

    camera_matrix = camera.GetTransformationMat
    light_shader_prog.Use()
    glUniformMatrix4fv(light_shader_prog._uniform_location["Camera_Projection"], 1, GL_TRUE, camera_matrix)
    glUniformMatrix4fv(light_shader_prog._uniform_location["Translation_Mat"], 1, GL_TRUE, cube.GetTranslationMat)
    glUniformMatrix4fv(light_shader_prog._uniform_location["Scale_Mat"], 1, GL_TRUE, cube.GetScaleMat)
    cube._vao.Bind()
    glDrawElements(GL_TRIANGLES, len(cube._indices), GL_UNSIGNED_INT, ctypes.c_void_p(0))
    
    
    shader_prog.Use()
    glUniformMatrix4fv(shader_prog._uniform_location["Camera_Projection"], 1, GL_TRUE, camera_matrix)
    glUniformMatrix4fv(shader_prog._uniform_location["Translation_Mat"  ], 1, GL_TRUE, np.identity(4))

    # rot_mat = np.array(GetRotationMat4(fuvector(0, 1, 0), np.radians(10 * t)), dtype = np.float32)
    # glUniformMatrix4fv(shader_prog._uniform_location["Rotation_Mat"], 1, GL_TRUE, rot_mat)
    
    glUniformMatrix4fv(shader_prog._uniform_location["Rotation_Mat"], 1, GL_TRUE, np.identity(4))
    glUniformMatrix4fv(shader_prog._uniform_location["Scale_Mat"], 1, GL_TRUE, np.identity(4))
    glUniform3f(shader_prog._uniform_location["LightSource"], *cube._pos)

    i = 0

    glUniform3f(shader_prog._uniform_location["view_pos"], *camera._pos)

    for mesh_name in mesh_manager._dict_name_mesh:
        mesh: Mesh = mesh_manager._dict_name_mesh[mesh_name]
        # Random color
        glUniform3f(shader_prog._uniform_location["RandomColor"], *colors[i])
        i += 1
        i = i % len(colors)

        # Ambient light color
        glUniform3f(shader_prog._uniform_location["Ka"], *mesh._mtl.Fetch(MATERIAL_SLOT.Ka, fvector(1, 1, 1)))
        # Diffuse light color
        glUniform3f(shader_prog._uniform_location["Kd"], *mesh._mtl.Fetch(MATERIAL_SLOT.Kd, fvector(1, 1, 1)))
        # Specular exponent
        glUniform1f(shader_prog._uniform_location["Ns"], mesh._mtl.Fetch(MATERIAL_SLOT.Ns, 20))
        # Specular light color
        glUniform3f(shader_prog._uniform_location["Ks"], *mesh._mtl.Fetch(MATERIAL_SLOT.Ks, fvector(1, 1, 1)))

        mesh._vao.Bind()
        glDrawElements(GL_TRIANGLES, len(mesh._indices), GL_UNSIGNED_INT, ctypes.c_void_p(0))


    pg.display.set_caption(f"{clock.get_fps() // 1}")
    pg.display.flip()
    clock.tick(0)

