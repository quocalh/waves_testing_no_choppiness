if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.dirname(__file__) + "/..")

import pygame as pg
from components.ibo import IBO
from components.texture import Texture, Texture2D


from meshes.mesh import Mesh, MeshManager
from meshes.material import Material, MaterialManager

mesh_manager = MeshManager(MaterialManager())

mesh_manager.ReadBothMaterialAndObjectFile(
    "", 
    "", 
    )