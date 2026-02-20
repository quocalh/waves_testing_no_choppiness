from OpenGL.GL import *
import numpy as np





SHADER_TYPE_MAPPING = {
    GL_VERTEX_SHADER: "VERTEX SHADER",
    GL_FRAGMENT_SHADER: "FRAGMENT SHADER",
}

class ShaderProgram:
    def __init__(self):
        self._ref = None
        self._vert_shader = None
        self._frag_shader = None

class Shader:
    __slots__ = ("_ref", "_src", "_is_detached")

    def __init__(self, shader_type, shader_src):
        self._ref = glCreateShader(shader_type)
        self._src: str = shader_src
        self._is_detached = False
        glShaderSource(self._ref, self._src)

    def Compile(self):
        glCompileShader(self._ref)
        compile_success = glGetShaderiv(self._ref, GL_COMPILE_STATUS)
        if not compile_success:
            error = glGetShaderInfoLog(self._ref)
            shader_type = glGetShaderiv(self._ref, GL_SHADER_TYPE)
            self.Delete()
            self.ShowSource()
            print(error)
            raise Exception(f"SHADERS:: COMPILATION ERROR :: {SHADER_TYPE_MAPPING[shader_type]}\n\tINFO LOG: {error}")
        
    def ShowSource(self):
        src = []
        counter = 1
        for line in self._src.splitlines():
            if line.strip():
                src.append(f"0({counter}) {line}")
            else:
                src.append(f"0({counter}) ")
            counter += 1
        print("\n".join(src))
    
    def Detach(self, prog_shader: ShaderProgram):
        glDetachShader(prog_shader._ref, self._ref)
        self._is_detached = True

    def Delete(self):
        if self._is_detached == False:
            print("[WARNING]: SICNE THE SHADER HASN'T BEEN DETEACHED YET, THIS DELETION COMMAND HAS NO EFFECT!")
        glDeleteShader(self._ref)

uniform_mapping_Matrixn_function_fv = {
    2: glUniformMatrix2fv,
    3: glUniformMatrix3fv,
    4: glUniformMatrix4fv,
}

uniform_mapping_function_fv = {
    1: glUniform1fv, 
    2: glUniform2fv, 
    3: glUniform3fv, 
    4: glUniform4fv, 
}
uniform_mapping_function_v = {
    1: glUniform1f,
    2: glUniform2f,
    3: glUniform3f,
    4: glUniform4f,
}

# idk, since i just have learnt about vert and frag shaders, idk how to handle this specifically
class ShaderProgram:
    
    __slots__ = ("_ref", "_vert_shader", "_frag_shader")

    def __init__(self, vertex_shader: Shader, fragment_shader: Shader):
        self._vert_shader = vertex_shader
        self._frag_shader = fragment_shader
        self.ShaderCheck()
        self._ref = glCreateProgram()

    def ShaderCheck(self):
        vert = glGetShaderiv(self._vert_shader._ref, GL_SHADER_TYPE)
        if vert != GL_VERTEX_SHADER:
            raise Exception(f"SHADER PROGRAM:: SHADER CHECK:: WE NEED A VERTEX SHADER")
        
        frag = glGetShaderiv(self._frag_shader._ref, GL_SHADER_TYPE)
        if frag != GL_FRAGMENT_SHADER:
            raise Exception(f"SHADER PROGRAM:: SHADER CHECK:: WE NEED A FRAGMENT SHADER")
    
    def LinkingShaders(self):
        glAttachShader(self._ref, self._vert_shader._ref)
        glAttachShader(self._ref, self._frag_shader._ref)
        glLinkProgram(self._ref)
        link_success = glGetProgramiv(self._ref, GL_LINK_STATUS)
        if not link_success:
            error = glGetProgramInfoLog(self._ref)
            self._vert_shader.Detach(self)
            self._frag_shader.Detach(self)
            self._vert_shader.Delete()
            self._frag_shader.Delete()
            self.Delete()
            raise Exception(f"SHADER PROGRAM::LINKING PROGRAMS:: \n\tINFO LOG: {error.decode("utf-8")}")
        self._vert_shader.Detach(self)
        self._frag_shader.Detach(self)
        self._vert_shader.Delete()
        self._frag_shader.Delete()
        
    def SetBool(self, name, value: bool):
        location = glGetUniformLocation(self._ref, name)
        if location == - 1:
            print(f"Warning: Uniform {name} not found")
        glUniform1i(location, value)

    def SetFloat(self, name, value: float):
        location = glGetUniformLocation(self._ref, name)
        if location == -1:
            print(f"Warning: Uniform {name} not found")
        glUniform1f(location, value)

    def SetFloatArrayVector(self, name: str, length: int, stride: int, array: np.ndarray):
        """
        NOTE:
        name: shader_name
        length: length of a single vector
        stride: length of full array
        array: this one |only 1 array|, consisting of all v4 components, no multiple 2d arrays  
        """
        if array.shape != (length, ):
            raise Exception(f"not match the shape here: {array.shape} != {(length,)}")
        
        if stride % length != 0:
            raise Exception(f"")
        
        location = glGetUniformLocation(self._ref, name)
        if location == -1:
            raise Exception(f"Warning: nowhere has the var ({name}) been found")
        
        uniform_mapping_function_fv[length](location, stride // length, array)

    def SetFloatVector(self, name, array: np.ndarray):
        location = glGetUniformLocation(self._ref, name)
        if location == -1:
            raise Exception(f"nowhere have we found the ({name}) in the shader file")
        uniform_mapping_function_v[len(array)](location, *array)

    def SetInt(self, name: str, value: int):
        location = glGetUniformLocation(self._ref, name)
        if location == -1:
            raise Exception(f"nowhere have we found the name \"{name}\" in the shader file")
        glUniform1i(location, value)
    
    def SetMat(self, name: str, nxn: int, flatten_mat_array: np.ndarray, transpose = GL_TRUE, count: int = 1):
        # flatten_mat_arry = [[][][][], [][][][]] : this is two 2x2 matrixes
        location = glGetUniformLocation(self._ref, name)
        if location == -1:
            raise Exception(f"Warning: nowhere have we found the name \"{name}\" in the shader file")
        
        for i in range(len(flatten_mat_array)): 
            mat_row: np.ndarray = flatten_mat_array[i]
            if mat_row.shape != (nxn, ):
                raise Exception(f"misalignment in input shape: {mat_row.shape} vs {(nxn, nxn, )}")

        uniform_mapping_Matrixn_function_fv[nxn](location, count, transpose, flatten_mat_array)
    


    def Delete(self):
        glDeleteProgram(self._ref)
    
    def Use(self):
        glUseProgram(self._ref)
        
    def Unuse(self):
        glUseProgram(0)

