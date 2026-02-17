import sys
import os
from pyglm import glm

sys.path.append("..")

if __name__ == "__main__":
    sys.path.append("..")

from components.settings import *
from components.vbo import *
from components.vao import *
from components.shaders import *
from components.ibo import *
from abstraction.custom import *


class GraphicObject:
    """
    This object is created only to reduce the cubersome of 
        opening the vao, 
            createing, binding vbo ebo, 
                doing attrib pointer 
        and sealing the vao at the end (unbind it)
    This architecture would compress it into like 2 lines? given the indices (optional)i and the vertices (demanded)
    """
    __slots__ = (
        "_vbo", "_vao", "_ebo", 
        "_vertices", "_indices",
        "_pos", "_rot", "_scale",
                 )
    def __init__(self, vao_layout: AttributeLayout):
        self._vao = VAO(vao_layout)
        self._vbo = VBO()
        self._ebo = IBO()
        
        self._vertices = None
        self._indices = None

        self._pos = np.zeros(3, dtype = np.float32)
        self._rot = np.identity(4)
        self._scale = 1

    @property
    def GetTranslationMat4(self):
        return GetTranslationMat4(self._pos)

    @property
    def GetRotationMat4(self):
        return self._rot
    
    @property
    def GetScaleMat4(self):
        return GetScaleMat4(self._scale)
    
    @property
    def GetModelMatrix(self):
        # extrinsic rot -> scale em, rotating, then translate em
        return self.GetTranslationMat4 @ self.GetRotationMat4 @ self.GetScaleMat4

    def SetRotationMat4(self, axis: np.ndarray, radian: float, dtype = np.float32):
        self._rot = np.array(glm.rotate(radian, axis), dtype = dtype)

    def Setup(self, vertices: np.ndarray, indices: np.ndarray = np.ndarray, usage = GL_STATIC_DRAW):
        assert indices.dtype == np.uint32, "np.uint32 pls :sob:"
        self._vertices = vertices
        if type(indices) == np.ndarray:
            self._indices = indices
            
            self._vao.Bind()
            self._vbo.Bind(GL_ARRAY_BUFFER)
            self._ebo.Bind(GL_ELEMENT_ARRAY_BUFFER)

            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, usage)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, usage)

            self._vao.SetUpVertexArray()
            self._vao.Unbind()
            self._vao.Unbind()
        else:
            self._vao.Bind()
            self._vbo.Bind(GL_ARRAY_BUFFER)
            self._ebo.Bind(GL_ELEMENT_ARRAY_BUFFER)
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, usage)
            self._vao.SetUpVertexArray()
            self._vbo.Unbind()
            self._vao.Unbind()
    

class FundamentalShadersSet:
    __slots__ = ("_shader_prog", "_shaders_", "_shaders_src")
    def __init__(self):
        self._shader_prog: ShaderProgram = None

        self._shaders_ = {
            GL_FRAGMENT_SHADER: None,
            GL_VERTEX_SHADER: None, 
        }
        self._shaders_src = {
            GL_FRAGMENT_SHADER: "",
            GL_VERTEX_SHADER: "", 
        }
    
    def CreateProgram(self, directory: str):
        vert_src, frag_src = ReadShaderFile(directory)
        self._shaders_src[GL_VERTEX_SHADER] = vert_src
        self._shaders_src[GL_FRAGMENT_SHADER] = frag_src
        self._shaders_[GL_VERTEX_SHADER] = Shader(GL_VERTEX_SHADER, vert_src)
        self._shaders_[GL_FRAGMENT_SHADER] = Shader(GL_FRAGMENT_SHADER, frag_src)
        self._shaders_[GL_VERTEX_SHADER].Compile(); self._shaders_[GL_FRAGMENT_SHADER].Compile()
        self._shader_prog = ShaderProgram(self._shaders_[GL_VERTEX_SHADER], self._shaders_[GL_FRAGMENT_SHADER])
        self._shader_prog.LinkingShaders()
        

    def SetUpShader(self, shader_type, shader_src: str):
        self._shaders_[shader_type] = Shader(shader_type, shader_src)
        self._shaders_src[shader_type] = shader_src

    @property
    def vert(self):
        return self._shaders_[GL_VERTEX_SHADER]
    @property
    def frag(self):
        return self._shaders_[GL_FRAGMENT_SHADER]
    
    @property
    def vert_src(self):
        return self._shaders_src[GL_VERTEX_SHADER]
    @property
    def frag_src(self):
        return self._shaders_src[GL_FRAGMENT_SHADER]

    def LinkingProgram(self):
        assert self.vert != "", f"lack of vertex shader"
        assert self.frag != "", f"lack of vertex shader"
        vert, frag = self.vert, self.frag

        self._shader_prog = ShaderProgram(vert, frag)
        vert.Compile()
        frag.Compile()
        self._shader_prog.LinkingShaders()







        