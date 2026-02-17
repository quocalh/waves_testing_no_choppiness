from OpenGL.GL import *

if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.dirname(__file__) + "/..")

from components.shaders import Shader, ShaderProgram

def CreateShaderProgram(directory: str):
    vert_src, frag_src = ReadShaderFile(directory)
    vert = Shader(GL_VERTEX_SHADER, vert_src)
    frag = Shader(GL_FRAGMENT_SHADER, frag_src)
    vert.Compile()
    frag.Compile()
    prog = ShaderProgram(vert, frag)
    prog.LinkingShaders()
    return prog

def ReadShaderFile(shader_src_directory: str):
    """
    NOTE: 
    the shader src file must follow these syntax
        Begin of Vertex shader: #VERTEXSHADER
        Begin of Fragment shader: #FRAGMENTSHADER

    The function will omit an error if not found either of these
    """
    with open(shader_src_directory) as file:
        vertex_src = ""
        fragment_src = "" 
        lines = file.readlines()

        str_pnt = None

        for line in lines:
            
            if line.strip() == "// VERTEX SHADER":
                str_pnt = "v"
                continue
            elif line.strip() == "// FRAGMENT SHADER":
                str_pnt = "f"
                continue

            if str_pnt == "v":
                vertex_src += line
            elif str_pnt == "f":
                fragment_src += line
                
        if not vertex_src:
            raise Exception("READING SHADER FILE:: HAVEN'T FOUND THE #VERTEXSHADER")
        
        if not fragment_src:
            raise Exception("READING SHADER FILE:: HAVEN'T FOUND THE #FRAGMENTSHADER")
        
        return vertex_src, fragment_src

