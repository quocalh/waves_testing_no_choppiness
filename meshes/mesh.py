import numpy as np

if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.dirname(__file__ + "/.."))

from OpenGL.GL import *

from meshes.material import MaterialManager



class Mesh:
    pass

from components.vbo import VBO
from components.ibo import IBO
from components.vao import VAO, Layout, AttributeLayout
from meshes.material import *
class MeshManager:
    pass

class Mesh:
    _triangle_to_triangle_indices: np.ndarray = np.array([0, 1, 2], dtype = np.uint32)
    _quad_to_triangle_indices: np.ndarray = np.array([0, 1, 2, 0, 2, 3], dtype = np.uint32)
    def __init__(self):
        self._vertices: np.ndarray | np.float32 = []
        self._indices: np.ndarray | np.uint32 = []
        self._name: str = None
    
        self._mesh_manager: MeshManager = None
        self._mtl: Material = None

        self._vbo: VBO = None
        self._vao: VAO = None
        self._ibo: IBO = None
        self._attrib_layout: AttributeLayout = AttributeLayout([
            Layout(3, np.float32), # position
            Layout(2, np.float32), # texcoord
            Layout(3, np.float32)  # normal
        ])

        self._index_pnt: int = 0
        self._s: int = None

        self._pos: np.ndarray = np.array([0, 0, 0], dtype = np.float32)
        self._orientation: np.ndarray = np.array([0, 0, 1], dtype = np.float32)
        self._rot: np.ndarray = np.identity(4)
        self._scale: float = 1
        
    @property
    def GetRotMat(self):
        return self._rot
    
    @property
    def GetScaleMat(self):
        s = self._scale
        return np.array([
            [s, 0, 0, 0],
            [0, s, 0, 0],
            [0, 0, s, 0],
            [0, 0, 0, 1],
        ], dtype = np.float32)
    
    @property
    def GetTranslationMat(self):
        p = self._pos
        return np.array([
            [1, 0, 0, p[0]],
            [0, 1, 0, p[1]],
            [0, 0, 1, p[2]],
            [0, 0, 0,  1  ],
        ], dtype = np.float32)

    def add_vertex_strips(self, stride: list[str], mesh_manager: MeshManager):
        self._mesh_manager = mesh_manager

        # prefix = stride[0]        
        # elif prefix == "f":
        p = mesh_manager._pos_catalog
        t = mesh_manager._tex_catalog
        n = mesh_manager._norm_catalog

        # vertices
        for i in range(1, len(stride)):
            id_strip: list[int] = stride[i].split("/")
            iPos, iTex, iNorm = int(id_strip[0]) - 1, int(id_strip[1]) - 1, int(id_strip[2]) - 1
            Pos, Tex, Norm = p[iPos], t[iTex], n[iNorm]
            vertices_strip: list[float] = (*Pos, *Tex, *Norm)
            self._vertices.append(vertices_strip)

        # indices
        for i in range(1, len(stride) - 2):
            self._indices.append(self._index_pnt)
            self._indices.append(self._index_pnt + i)
            self._indices.append(self._index_pnt + i + 1)
        self._index_pnt += len(stride) - 1

    def OpenGL_contruct(self):
        self._vao = VAO(self._attrib_layout)
        self._vao.Bind()

        self._vbo = VBO()
        self._vbo.Bind(GL_ARRAY_BUFFER)
        
        self._ibo = IBO()
        self._ibo.Bind(GL_ELEMENT_ARRAY_BUFFER)
        
        glBufferData(
            GL_ARRAY_BUFFER, self._vertices.nbytes, self._vertices, GL_STATIC_DRAW
            )
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER, self._indices.nbytes, self._indices, GL_STATIC_DRAW
            )
        
        self._vao.SetUpVertexArray()

        self._vao.Unbind()
        self._vbo.Unbind(GL_ARRAY_BUFFER)



class MeshManager:
    def __init__(self, mtl_manager: MaterialManager):

    
        self._pos_catalog: list[float] = []
        self._tex_catalog: list[float] = []
        self._norm_catalog: list[float] = []

        self._dict_name_mesh: dict[str: Mesh] = {}
        self._binding_mesh: Mesh = None
        
        self._mtl_manager: MaterialManager = mtl_manager

        self._dict_prefix_function: dict[str: function] = {
            "o": self.BindingMesh,
            "v": self.Read_Vertex,
            "vn": self.Read_Vertex_Normal,
            "vt": self.Read_Vertex_TexCoord,
        }
        self._s: int = None

    
    def BindingMesh(self, stride: list[str]):
        name = stride[1]
        if name not in self._dict_name_mesh:
            self._dict_name_mesh[name] = Mesh()
            self._dict_name_mesh[name]._name = name
            
        self._binding_mesh = self._dict_name_mesh[name]

    def UnbindingMesh(self):
        self._binding_mesh = None

    def Read_Vertex_Normal(self, stride: list[str]):
        self._norm_catalog.append(
            (float(stride[1]), float(stride[2]), float(stride[3]))
        )

    def Read_Vertex(self, stride: list[str]):
        self._pos_catalog.append(
            (float(stride[1]), float(stride[2]), float(stride[3]))
        )

    def Read_Vertex_TexCoord(self, stride: list[str]):
        self._tex_catalog.append(
            (float(stride[1]), float(stride[2]))
        )

    def ReadObjectFile(self, obj_directory: str):
        with open(obj_directory, "r") as f:
            script = f.read().split("\n")
        
        for str_stride in script:
            stride = str_stride.split(" ")
            prefix: str = stride[0]

            # blank
            if prefix == "":
                continue
            
            # comments
            elif prefix == "#":
                continue
            elif prefix == "s":
                # print(stride[1] in ("off", ))
                if stride[1] in ("off",):
                    self._s = 1
                else:    
                    self._s = int(stride[1])

            elif prefix == "o":
                self.BindingMesh(stride)

            elif prefix == "usemtl":
                
                name = stride[1]
                self._binding_mesh._mtl = self._mtl_manager._dict_name_mtl[name]
            
            # i have no idea how to handle this one
            elif prefix == "mtllib": 
                self._mtl_manager._name = stride[1]

            else:
                if prefix in self._dict_prefix_function:
                    method = self._dict_prefix_function[prefix]
                    method(stride)
                else:
                    self._binding_mesh.add_vertex_strips(stride, self)
                
        self._pos_catalog = np.array(self._pos_catalog, dtype = np.float32)
        self._tex_catalog = np.array(self._tex_catalog, dtype = np.float32)
        self._norm_catalog = np.array(self._norm_catalog, dtype = np.float32)

        self.UnbindingMesh()

        for mesh_name in self._dict_name_mesh:
            mesh: Mesh = self._dict_name_mesh[mesh_name]
            mesh._vertices = np.array(mesh._vertices, dtype = np.float32)
            mesh._indices = np.array(mesh._indices, dtype = np.uint32)
    
    def ReadMaterialFile(self, mtl_directory: str):
        self._mtl_manager.ReadMaterialFile(mtl_directory)
    
    def ReadBothMaterialAndObjectFile(self, material_directory: str, object_directory: str):
        self.ReadMaterialFile(material_directory)
        self.ReadObjectFile(object_directory)

    def Reset(self):
        pass