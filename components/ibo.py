import numpy as np

from OpenGL.GL import *

class IBO:
    __slots__ = ("_ref")
    def __init__(self):
        self._ref = glGenBuffers(1)
        
    def Bind(self, target = GL_ELEMENT_ARRAY_BUFFER):
        glBindBuffer(target, self._ref)
    
    def Unbind(self, target = GL_ELEMENT_ARRAY_BUFFER):
        glBindBuffer(target, 0)
    
    def Delete(self):
        glDeleteBuffers(self._ref)
        