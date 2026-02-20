

if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.dirname(__file__) + "/..")

import pygame as pg
from OpenGL.GL import *
from types import FunctionType
from collections.abc import Callable
import numpy as np

from components.shaders import ShaderProgram, Shader

# ENUMS
from enum import Enum


class UNIFORM(Enum):
    DOUBLE = 0
    FLOAT = 1
    INT = 2
    UINT = 3

    VEC2 = 4
    VEC3 = 5
    VEC4 = 6

    ARRAY_VEC2 = 7
    ARRAY_VEC3 = 8
    ARRAY_VEC4 = 9

    MAT4 = 10
    MAT3 = 11
    MAT2 = 12

# i fucking know there is a way to do this more elegantly, but i can't think of
UNIFORM_FUNCTION: dict[UNIFORM: Callable] = {
    UNIFORM.DOUBLE: glUniform1d, 
    UNIFORM.FLOAT: glUniform1f,
    UNIFORM.INT: glUniform1i, 
    UNIFORM.UINT: glUniform1ui,

    UNIFORM.VEC2: glUniform2f, 
    UNIFORM.VEC3: glUniform3f, 
    UNIFORM.VEC4: glUniform4f, 

    UNIFORM.ARRAY_VEC2: glUniform2fv,
    UNIFORM.ARRAY_VEC3: glUniform3fv,
    UNIFORM.ARRAY_VEC4: glUniform4fv,

    UNIFORM.MAT4: glUniformMatrix4fv,
    UNIFORM.MAT3: glUniformMatrix3fv,
    UNIFORM.MAT2: glUniformMatrix2fv,
}

UNIFORM_DIMENSION: dict[UNIFORM: int] = {
    UNIFORM.DOUBLE: 1,
    UNIFORM.FLOAT: 1,
    UNIFORM.INT: 1, 
    UNIFORM.UINT: 1,

    UNIFORM.VEC2: 2, 
    UNIFORM.VEC3: 3, 
    UNIFORM.VEC4: 4, 

    UNIFORM.ARRAY_VEC2: 2,
    UNIFORM.ARRAY_VEC3: 3,
    UNIFORM.ARRAY_VEC4: 4,

    UNIFORM.MAT4: 4,
    UNIFORM.MAT3: 3,
    UNIFORM.MAT2: 2,
}

class ShaderProgramUniformPackage:
    def __init__(self, name: str, data_type_enum: UNIFORM, index: int = None):

        self._name: str = None
        self._uniform_location: int = None
        self._data : any = None
        
        self._data_type_enum: UNIFORM = data_type_enum

        self._is_a_static_uniform: bool = False
        self._index: int = index


"""
mesh.["name"].UpdateUniform(___, ___, ___)
faster, not readable

program_shader.SetUniformXX(____, _____, _____)
readable, slowasf, 

good for automatic?
    -> combine

"""
    
from collections.abc import Iterable

class Uniform:
    def __init__(self, name, static, reset):
        self._static: bool
        self._reset: bool
        self._name: str
        self._location: int

class TestingShaderProgram(ShaderProgram):
    def __init__(self, vertex_shader, fragment_shader, uniform_names_set: Iterable[str]):
        super().__init__(vertex_shader, fragment_shader)
        # self._dynamic_uniforms: list[ShaderProgramUniformPackage] = []
        # self._static_uniforms: list[ShaderProgramUniformPackage] = [] 

        self._uniform_names: set = uniform_names_set
        self._uniform_location: dict[str: int] = {}

        self.LinkingShaders()
        self.FetchUniformLocations()

    def FetchUniformLocations(self):
        for name in self._uniform_names:
            self.GetLocation(name)
    
    def GetLocation(self, name, warning_flag = True):
        location: int = glGetUniformLocation(self._ref, name)
        if location == -1 and warning_flag:
            print(f"[warning]: {name} was either not found or not used in the shader")

        self._uniform_location[name] = location
        return location

    def UserGetUniformLocation(self, name):
        if name in self._uniform_location:
            return self._uniform_location[name]
        
        location = self.GetLocation(name)
        # if location == -1:
        #     print(f"SHADER PROG ({name}): trying to gain access to nil?")
        #     raise(f"SHADER PROG ({name}): trying to gain access to nil?\n")
        
        return location
        
    
    