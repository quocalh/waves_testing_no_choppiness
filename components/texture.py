from OpenGL.GL import * 
import OpenGL.GL as gl
import pygame as pg
from enum import Enum
import numpy as np

from components.shaders import ShaderProgram
"""
Hmm, indeed a phenomenon:

RETRIVIAL FUNCTIONS: 
glGetTexParameteriv(ref, )
glGetShaderiv(ref, GL_COMPILE_STATUS)
glGetProgramiv(ref, GL_LINK_STATUS)

MODIFYING FUNCTIONS: SETTING UP 
#                     class          function          attrib
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
"""

class TexFeat(Enum):
    GL_TEXTURE_MIN_FILTER = 0
    GL_TEXTURE_MAG_FILTER = 1
    GL_TEXTURE_WRAP_S = 2
    GL_TEXTURE_WRAP_T = 3
    GL_TEXTURE_WRAP_R = 3

class Texture:
    @staticmethod
    def SetTexture2DAttributes(target = GL_TEXTURE_2D, wrap_s = GL_REPEAT, wrap_t = GL_REPEAT, min = GL_NEAREST, mag = GL_NEAREST, border_color: np.ndarray = np.zeros(4, dtype = np.float32)):
        """
        THIS IS USED TO SETUP ATTRIBS FOR EVERY BINDED? YES
        """
        glTexParameteri(target, GL_TEXTURE_WRAP_S, wrap_s)
        glTexParameteri(target, GL_TEXTURE_WRAP_T, wrap_t)
        if wrap_s == GL_CLAMP_TO_BORDER or wrap_t == GL_CLAMP_TO_BORDER:
            glTexParameterfv(target, GL_TEXTURE_BORDER_COLOR)
        glTexParameteri(target, GL_TEXTURE_MIN_FILTER, min)
        glTexParameteri(target, GL_TEXTURE_MAG_FILTER, mag)
    


class Texture2D(Texture):
    __slots__ = ("_ref", "_surface", "_str_buffer")
    """
    fundamental setups:
        GL_TEXTURE_WRAP_S
        GL_TEXTURE_WRAP_T
            GL_REPEAT
            GL_CLAMP_TO_EDGE
            GL_CLAMP_TO_BORDER / GL_TEXTURE_BORDER_COLOR_fv
            GL_MIRRORER_REPEAT

        GL_MIN_FILTER
        GL_MAG_FILTER
            GL_LINEAR
            GL_NEAREST

    glGenerateMipMaps(GL_TEXTURE_2D)

    modifying
        GL_MIN_FILTER
        GL_MAG_FILTER
            GL_NEAREST_MIPMAP_NEAREST: 
                takes the nearest mipmap to match the pixel size and 
                uses nearest neighbor interpolation for texture sampling.
            GL_LINEAR_MIPMAP_NEAREST: 
                takes the nearest mipmap level and samples that level
                using linear interpolation.
            GL_NEAREST_MIPMAP_LINEAR: 
                linearly interpolates between the two mipmaps that
                most closely match the size of a pixel and samples the interpolated level via nearest neighbor
                interpolation.
            GL_LINEAR_MIPMAP_LINEAR: 
                linearly interpolates between the two closest mipmaps
                and samples the interpolated level via linear interpolation.

    NOTE: this should be documented, observed carefully
        modifying nature:
            gentext
            gentext

            Bind()
            Bind()
                Modify, caching attrib
            Unbind()
            Unbind()
            
            glUseProgram
            Uniform()
            

    """
    def __init__(self, source: str):
        self._ref = glGenTextures(1, )
        self._surface = self.LoadImage(source)
        self._str_buffer = self.GetSurfaceStringBuffer()
    
    def Construct(self, wrap_s = GL_REPEAT, wrap_t = GL_REPEAT, min = GL_NEAREST, mag = GL_NEAREST):
        self.Bind(GL_TEXTURE_2D)
        self.SetTexture2DAttributes(GL_TEXTURE_2D, wrap_s, wrap_t, min, mag)
        self.GenerateTexture(GL_TEXTURE_2D, 0, GL_RGBA, self._surface.width, self._surface.height, GL_RGBA, GL_UNSIGNED_BYTE)
        glGenerateMipmap(GL_TEXTURE_2D)
        self.Unbind(GL_TEXTURE_2D)

    def GenerateTexture(self, target, level, storing_format, w, h, source_format = GL_RGBA, source_dtype = GL_UNSIGNED_BYTE):
        if not self._str_buffer:
            print(self._str_buffer)
            raise Exception("Failed to generate image from a invalid string buffer")
        
        if len(self._str_buffer) != w * h * 4: # width * height * bytesize
            print(f"Warning: Buffer mismatch: {w * h * 4} vs {len(self._str_buffer)}")
        # my stupid ahh thought it must be GL_UNSIGNED_INT 
        glTexImage2D(target, level, storing_format, w, h, 0,
                     source_format, source_dtype, self._str_buffer)
        

    def LoadImage(self, directory: str):
        return pg.image.load(directory).convert_alpha()

    def GetSurfaceStringBuffer(self, format = "RGBA", flipped = True):
        return pg.image.tobytes(self._surface, format, flipped)




    def Bind(self, target = GL_TEXTURE_2D):
        glBindTexture(target, self._ref)
    
    def Unbind(self, target = GL_TEXTURE_2D):
        glBindTexture(target, 0)



    
    def Uniform(self, prog_shader: ShaderProgram, name, texture_id):
        prog_shader.SetInt(name, texture_id)
    
def ActivateTextureSlot(tex_id_slot:  int = GL_TEXTURE0):
    glActiveTexture(tex_id_slot)
    

class Texture2DArray(Texture):
    __slots__ = ("_ref", "_tex_directories")
    def __init__(self, src_list: list[str]):
        self._ref = glGenTextures(1, )
        self._tex_directories: list[str] = src_list
    
    def LoadImage(self, directory: str):
        self._tex_directories.append(directory)

    
    def Bind(self, target = GL_TEXTURE_2D_ARRAY):
        glBindTexture(target, self._ref)
    
    def Unbind(self):
        glBindTexture(GL_TEXTURE_2D_ARRAY, 0)

    def Construct(self, wrap_s = GL_REPEAT, wrap_t = GL_REPEAT, min = GL_NEAREST, mag = GL_NEAREST):
        self.Bind(GL_TEXTURE_2D_ARRAY)
        self.SetTextureAttributes(wrap_s, wrap_t, min, mag)
        width, height = 0, 0
        glTexImage3D(
            GL_TEXTURE_2D_ARRAY,
            0, 
            GL_RGBA, 
            width, height
        )
        self.Unbind()

    def SetTextureAttirbutes(self, wrap_s, wrap_t, min, mag):
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, wrap_s)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, wrap_t)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, min)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, mag)
    
    
    
