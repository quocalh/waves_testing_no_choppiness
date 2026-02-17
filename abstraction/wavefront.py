import numba as nb
from OpenGL.GL import *
import pygame as pg
import numpy as np

import os
import sys


if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__) + "/..")

from components.vbo import VBO
from components.vao import VAO, AttributeLayout, Layout
from components.texture import Texture, Texture2D, Texture2DArray
from components.ibo import IBO

from components.shaders import Shader

from abstraction.object import FundamentalShadersSet

"""
shader will be handled by models
    in the shader we have
        layout (obj): 
            position
            normal
            texcoord
            * texture id (texture2d array) # might be discarded
            
        uniform (mtl): 
            spec
                spec exp
            diff
            ambient
            alpha
            emissive
            index of refraction (nah...)
            illumination
            transparency
            texture with id?
"""


def get_str_from_file(directory: str):
    str_array: list[str]  = []
    with open(directory, "r") as f:
        str_array = f.read().split("\n")
    return str_array


class Material:
    pass

class MaterialManager:
    __slots__ = ("_dict_name_mtl", "_binding_mtl", "_filled", "_name")
    def __init__(self):
        self._dict_name_mtl: dict[str: Material] = {}
        self._binding_mtl: Material = None
        self._filled: bool = False

        self._name: str = None

    def Bind(self, name: str):
        self._dict_name_mtl[name] = Material()
        self._binding_mtl = self._dict_name_mtl[name] # passing the reference

    def Read_mtl_file(self, mtl_directory: str):
        with open(mtl_directory, "r") as f:
            script = f.read().split("\n")
        for stride in script:
            stride = stride.split(" ")
            if not stride[0]:
                continue
            elif stride[0] == "#":
                continue

            prefix = stride[0]
            if prefix == "newmtl":     
                name = stride[1]
                self.Bind(name)
                self._binding_mtl._name = name
            
            else:  
                self._binding_mtl.add(stride)
        f.close()
        self._filled = True


class Material:
    __slots__ = ("_Ns", "_Ka", "_Kd", "_Ks", "_Ke", "_Ni", "_d", "_illum", "_name")
    def __init__(self) -> Material:
        self._Ns: int           = None
        self._Ka: np.ndarray    = None
        self._Kd: np.ndarray    = None
        self._Ks: np.ndarray    = None
        self._Ke: np.ndarray    = None
        self._Ni: np.ndarray    = None
        self._d: float          = None
        self._illum: int        = None

        self._name: str = None

    def add(self, stride: list[str]):
        prefix = stride[0]
        if prefix == "Ns":
            self._Ns = float(stride[1])
        elif prefix == "Ka":
            self._Ka = np.array([float(stride[1]), float(stride[2]), float(stride[3])], dtype = np.float32)
        elif prefix == "Kd":
            self._Kd = np.array([float(stride[1]), float(stride[2]), float(stride[3])], dtype = np.float32)
        elif prefix == "Ks":
            self._Ks = np.array([float(stride[1]), float(stride[2]), float(stride[3])], dtype = np.float32)
        elif prefix == "Ke":
            self._Ke = np.array([float(stride[1]), float(stride[2]), float(stride[3])], dtype = np.float32)
        elif prefix == "Ni":
            self._Ni = float(stride[1])
        elif prefix == "d":
            self._d = float(stride[1])
        elif prefix == "illum":
            self._illum = int(stride[1])
        
    
class Mesh:
    pass

class MeshManager:
    def __init__(self, mtl_manager: MaterialManager):

        self._pos_catalog: np.ndarray | np.float32 = []
        self._norm_catalog: np.ndarray | np.float32 = []
        self._tex_catlog: np.ndarray | np.float32 = []

        self._dict_name_mesh: dict[str: Mesh] = {}
        self._binding_mesh: Mesh = None
        self._mtl_manager: MaterialManager = mtl_manager

        self._textures: Texture2D
        # shall we make it a texture 2d array?

    def BindMesh(self, name: str):
        if name not in self._dict_name_mesh:
            new_mesh = Mesh()
            new_mesh._name = name
            self._dict_name_mesh[name] = new_mesh
        self._binding_mesh = self._dict_name_mesh[name]
    
    def Unbind(self):
        self._binding_mesh = None

    def Read_obj_file(self, obj_directory: str):
        with open(obj_directory, "r") as f:
            script = f.read().split("\n")
        
        
        for i in range(len(script)):
            
            stride = script[i].split(" ")
            prefix = stride[0]
            if prefix == "":
                continue
            if prefix == "#":
                continue

            elif prefix == "mtllib":
                self._mtl_manager._name = stride[1]
            
            elif prefix == "o":
                name = stride[1]
                self.BindMesh(name)

            elif prefix == "usemtl":
                name = stride[1]
                self._binding_mesh._mtl = self._mtl_manager._dict_name_mtl[name]

            elif prefix == "v":
                vec3 = (float(stride[1]), float(stride[2]), float(stride[3]))
                self._pos_catalog.append(vec3)
            elif prefix == "vn":
                vec3 = (float(stride[1]), float(stride[2]), float(stride[3]))
                self._norm_catalog.append(vec3)
            elif prefix == "vt":
                vec3 = (float(stride[1]), float(stride[2]))
                self._tex_catlog.append(vec3)
            else:
                self._binding_mesh.add(stride, self)

        # converting catalogs into numpy array for faster allocation (the straight-forward approach)
        self._pos_catalog = np.array(self._pos_catalog, dtype = np.float32)
        self._tex_catlog = np.array(self._tex_catlog, dtype = np.float32) 
        self._norm_catalog = np.array(self._norm_catalog, dtype = np.float32)

        self.Unbind()

        for mesh_name in self._dict_name_mesh:
            mesh: Mesh = self._dict_name_mesh[mesh_name]
            mesh._vertices = np.array(mesh._vertices, dtype = np.float32)
            mesh._indices = np.array(mesh._indices, dtype = np.uint32)

class Mesh:
    # OBJ file
    _triangle_to_triangle_indices: np.ndarray = np.array([0, 1, 2], dtype = np.uint32)
    _quad_to_triangle_indices: np.ndarray = np.array([0, 1, 2, 0, 2, 3], dtype = np.uint32)
    def __init__(self):
        self._s: int = None

        self._name: str = None
        self._vertices: np.ndarray = []
        self._indices: np.ndarray = []
        self._mtl: Material = None

        self._index_pnt = 0
        self._mesh_manager: MeshManager = None

        # graphical stuffs
        self._attrib_layout = AttributeLayout([
            Layout(3, np.float32), Layout(2, np.float32), Layout(3, np.float32)
        ])
        
    
    def add(self, stride: list[str], mesh_manager: MeshManager):
        self._mesh_manager = mesh_manager
        
        prefix = stride[0]
        if prefix == "s":  # smoothness
            self._s = float(stride[1])

        elif prefix == "f": # ibo and vertex merging
            p = self._mesh_manager._pos_catalog
            t = self._mesh_manager._tex_catlog
            n = self._mesh_manager._norm_catalog
            
            #  (pos_id/tex_id/normal_id)   (pos_id/tex_id/normal_id)   (pos_id/tex_id/normal_id)   (pos_id/tex_id/normal_id) 
            for i in range(1, len(stride)):
                vertex_id_strip: str = stride[i] # (pos_id/tex_id/normal_id) 
                p_i, t_i, n_i = (vertex_id_strip.split("/"))
                pos, tex, normal = p[int(p_i) - 1], t[int(t_i) - 1], n[int(n_i) - 1]
                vertex_strip: list[float] = (
                    *pos, *tex, *normal
                )
                self._vertices.append(vertex_strip)

            if len(stride) == 4:
                indices_offset = self._triangle_to_triangle_indices
            elif len(stride) == 5:
                indices_offset = self._quad_to_triangle_indices
            
            for offset in indices_offset:
                self._indices.append(self._index_pnt + offset)

            self._index_pnt += len(stride) - 1


    def OpenGLConstruct(self):
        self._vao = VAO(self._attrib_layout)
        self._vbo = VBO()
        self._ibo = IBO()

        self._vao.Bind()
        self._vbo.Bind(GL_ARRAY_BUFFER)
        self._ibo.Bind(GL_ELEMENT_ARRAY_BUFFER)

        glBufferData(GL_ARRAY_BUFFER, self._vertices.nbytes, self._vertices, GL_STATIC_DRAW)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._indices.nbytes, self._indices, GL_STATIC_DRAW)
        
        self._vao.SetUpVertexArray()

        self._vao.Unbind()
        self._vbo.Unbind()

        
        




class Scene:
    def __init__(self):
        self._models: list[MeshManager] = []
        self._shader: FundamentalShadersSet = None

        self._uniforms: dict[str: object] = {}        

        # same shaders
        # a subscription system for shaders (Component subscription, data streaming)
        # texture manager (GL_Active_texture; bind texture) // texture 2d arary

        # before doing allat
        # let's
            # opengl debugger / error handling
            # texture 2d array
            # uniform component driver -> data streaming, texture, uniform handling 
                # Mesh-without-loading reconstruct
            # optimizing
            # testing .obj waverfront file without texture
                # with textures
            


    def Draw(self):
        pass
    
    def CacheModel(self, file_name: str, directory: str):
        pass


if __name__ == "__main__":
    import pygame as pg
    from OpenGL.GL import *
    from pygame.locals import *

    pg.init()
    screen = pg.display.set_mode((800, 800), DOUBLEBUF | OPENGL)

    model = MaterialManager()
    model.Read_mtl_file(r"resources\obj_files\obj\holy_cube\cclc.mtl")

    mesh_manager = MeshManager(model)
    mesh_manager.Read_obj_file(r"resources\obj_files\obj\holy_cube\cclc.obj")


    print(mesh_manager._mtl_manager._dict_name_mtl)
    mat_: Material = mesh_manager._mtl_manager._dict_name_mtl["Material"]
    mat_1: Material = mesh_manager._mtl_manager._dict_name_mtl["Material.001"]
    print(mesh_manager._dict_name_mesh)


    for mesh_name in mesh_manager._dict_name_mesh:
        print(mesh_name)
    
    
    mesh_manager
    cube: Mesh = mesh_manager._dict_name_mesh["Cube"]
    # print(mesh_manager._norm_catalog)
    print("-------")
    print(cube._name)
    print(cube._indices)
    print(cube._vertices)

    print(cube._mtl._Ns)
    print(cube._mtl._Ka)
    print(cube._mtl._Kd)
    print(cube._mtl._Ks)
    print(cube._mtl._Ke)
    print(cube._mtl._Ni)
    print(cube._mtl._d)
    print(cube._mtl._illum)
    print(cube._mtl._name)
    print("gan")
    print(cube._mtl is mesh_manager._mtl_manager._dict_name_mtl["Material"])

    cube: Mesh = mesh_manager._dict_name_mesh["Cube.001"]
    # print(mesh_manager._norm_catalog)
    print("-------")
    print(cube._name)
    print(cube._indices)
    print(cube._vertices)

    print(cube._mtl._Ns)
    print(cube._mtl._Ka)
    print(cube._mtl._Kd)
    print(cube._mtl._Ks)
    print(cube._mtl._Ke)
    print(cube._mtl._Ni)
    print(cube._mtl._d)
    print(cube._mtl._illum)
    print(cube._mtl._name)
    print("gan")
    print(cube._mtl is mesh_manager._mtl_manager._dict_name_mtl["Material"])



    glGetError()