# Requirement
required installed package to run:
    numpy
    pygame
    PyOpenGL PyOpenGL_accelerate
    PyOpenGL
    numba
    pyglm

# Introduction
This is the ocean simulation demo 

## The shader files (.glsl)
Located in the resouces/shader_sources/ folder
The glsl has both the vertex shader, and the fragment shader
    separated by the 
        // VERTEX SHADER
        // FRAGMENT SHADER


## The rigorous one 
![image](resources\images\rigorous.png)
which ultilzing the exact formulas shown in the Tessendorf's note, or at least creating something similar to it. For this one, we tried our best to replicate the Tessendorf's ocean without the FFT technique

The running file: running_program/**waves_rigourous.py**
    the shader file: resources/shader_sources/**waves_rigorous.glsl**

## The modified one
![image](resources\images\modified.png)
This one, aims for the most artistic looks of the mild-conditioned ocean, with heavily modified wave spectrum and coefficients

the running file: running_program/**waves_modified.py**
    the shader file: resources/shader_sources/ **waves_modified.glsl**

## The wave generator
Note that the unit vector generator generates a uniform set of wavevectors for the shader file (.glsl)


