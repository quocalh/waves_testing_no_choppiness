import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
import sys
if __name__ == "__main__":
    sys.path.append("..")

from components.settings import GL_VALUE_MAPPING


class Layout:
    __slots__ = ("_length", "_dtype", "_nbytes")
    def __init__(self, length: int, dtype: np.dtype = np.float32):
        self._length = length
        self._dtype = dtype
        self._nbytes = length * np.dtype(dtype).itemsize 

class AttributeLayout:
    __slots__ = ("_trays", "_stride")

    def __init__(self, trays: list[Layout]):
        self._trays: list[Layout] = trays
        self._stride = self.getStride()

    def getStride(self):
        stride = 0
        for layout in self._trays:
            stride += np.dtype(layout._dtype).itemsize * layout._length
        return stride

# [[1, 2, 3], [1, 2, 3, 4], [1, 2,]]
# [             stride            ]

def ManuallySettingUpVertexArray(index, array: np.ndarray, normalized: bool, stride: int, c_void_pnt: int):
    """
    NOTE: single-element values can be input as array with only 1 element:
        e.g. np.array([1, ], dtype = np.float32) 
    """
    glVertexAttribPointer(
        index, len(array), 
        GL_VALUE_MAPPING[array.dtype], 
        normalized, stride, ctypes.c_void_p(c_void_pnt)
        )
    glEnableVertexAttribArray(index)

class VAO:
    __slots__ = ("_ref", "_attrib_layout")

    def __init__(self, attrib_layout: AttributeLayout):
        self._ref = glGenVertexArrays(1)      
        self._attrib_layout: AttributeLayout = attrib_layout    
    
    def SetUpVertexArray(self):
        void_pnt = 0
        stride = self._attrib_layout._stride
        trays: list[Layout] = self._attrib_layout._trays
        
        for i in range(len(trays)):
            layout = trays[i]
            glVertexAttribPointer(i, layout._length, GL_VALUE_MAPPING[layout._dtype], GL_FALSE, stride, ctypes.c_void_p(void_pnt))
            glEnableVertexAttribArray(i)
            void_pnt += layout._nbytes

    def Bind(self):
        glBindVertexArray(self._ref)

    def Unbind(self):
        glBindVertexArray(0)

    def Delete(self):
        glDeleteVertexArrays(1, (self._ref, ))

