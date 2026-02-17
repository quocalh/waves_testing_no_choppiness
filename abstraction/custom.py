import numpy as np
from pyglm import glm
from OpenGL.GL import *
import sys
import os

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
    print(os.path.abspath(__file__))

from components.shaders import Shader, ShaderProgram

def array(py_array: list, dtype = np.dtype):
    return np.aray(py_array, dtype = dtype)
def vector(py_array: list, dtype = np.float32):
    return np.array(py_array, dtype = dtype)
def fvector(*vector, dtype = np.float32):
    return np.array([*vector], dtype = dtype)
def fuvector(*vector, dtype = np.float32): # float unit vectorss
    vector = [*vector]
    v = np.array(vector, dtype = dtype)
    return v / np.linalg.norm(v)

def normalize(numpy_vector: np.ndarray):
    return numpy_vector / np.linalg.norm(numpy_vector)



def GetTranslationMat4(v3: np.ndarray):
    return np.array([
        [1, 0, 0, v3[0]],
        [0, 1, 0, v3[1]],
        [0, 0, 1, v3[2]],
        [0, 0, 0,   1  ],
    ], dtype = np.float32)


world_normal = np.array([0, 1, 0], dtype = np.float32)
def GetViewMat4(orientaion: np.ndarray, inverted_z = False):
    # a quick way to create a random rotation
    if inverted_z == False: 
        z_coef = 1
    if inverted_z == True:
        z_coef = -1
    o = orientaion 
    # right
    r = np.cross(world_normal, o) 
    r = r / np.linalg.norm(r)
    # up
    u = np.cross(o, r) 
    o = z_coef * o
    return np.array([
        [r[0], u[0], o[0], 0],
        [r[1], u[1], o[1], 0],
        [r[2], u[2], o[2], 0],
        [  0 ,   0 ,   0 , 1],
    ], dtype = np.float32)


def GetModelMatrix(rot_mat4: np.ndarray, translation_mat4: np.ndarray, scale_mat4: np.ndarray = np.identity(4)):
    # rotate first then translate (extrinsic)
    return np.array( translation_mat4 @ rot_mat4, dtype = np.float32)

def GetScaleMat4(scale):
    s = scale
    return np.array([
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, s, 0],
        [0, 0, 0, 1],
    ], dtype = np.float32)

def GetRotationMat4(axis: np.ndarray, radian: float):
    return glm.rotate(radian, axis)

def GetQuaternionRotationMat4(axis: np.ndarray, radian: float):
    pass




