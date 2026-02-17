import numpy as np
from OpenGL.GL import *

WIDTH, HEIGHT = 1550, 800
FPS = 0

TOGGLE_IS_WIREFRAME_MODE = False
TOGGLE_TIME_STOP = False
TOGGLE_FLASHFLIGHT = True

GL_VALUE_MAPPING = {
    np.uint32   : GL_UNSIGNED_INT,
    np.float32  : GL_FLOAT,
    np.float64  : GL_DOUBLE,
    np.int32    : GL_INT,
}