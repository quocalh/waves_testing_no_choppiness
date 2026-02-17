from OpenGL.GL import *


class VBO:
    __slots__ = ("_ref", )

    def __init__(self):
        self._ref = glGenBuffers(1)
        
    def Bind(self, targets = GL_ARRAY_BUFFER):
        glBindBuffer(targets, self._ref)

    def Unbind(self, targets = GL_ARRAY_BUFFER):
        glBindBuffer(targets, self._ref)

    def Delete(self):
        glDeleteBuffers(1, (self._ref,))
    
    # def BufferData(self):
    #     glBufferData()