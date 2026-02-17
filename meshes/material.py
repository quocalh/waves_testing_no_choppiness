import pygame as pg

import os, sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__) + "/..")
from components.texture import Texture2D
import numpy as np

from enum import IntEnum
from dataclasses import dataclass

# class Material(dataclass):
#     index: int
#     is_texture: bool 
    # if i ever have to use this class for the uniform (no more int enum)

class MATERIAL_SLOT(IntEnum):
    # materials
    Ns          = 0
    Ka          = 1
    Kd          = 2
    Ks          = 3
    Ke          = 4
    Ni          = 5
    d           = 6
    illum       = 7
    # texture maps
    map_Kd      = 8
    map_Ks      = 9
    map_Ka      = 10
    map_Ns      = 11
    map_Bump    = 12
    map_d       = 13

class TEXTURE_SLOT(IntEnum):
    # disposal units
    null0       = 0
    null1       = 1
    null2       = 2
    null3       = 3
    null4       = 4
    null5       = 5
    null6       = 6
    null7       = 7
    # texture
    map_Kd      = 8
    map_Ks      = 9
    map_Ka      = 10
    map_Ns      = 11
    map_Bump    = 12
    map_d       = 13



class Material:

    _PREFIX_TO_SLOT_INDEX: dict[str, MATERIAL_SLOT] = {
            slot.name: slot for slot in MATERIAL_SLOT
        }

    def __init__(self):
        self._Ns: float             = None
        self._Ka: np.ndarray        = None
        self._Kd: np.ndarray        = None
        self._Ks: np.ndarray        = None
        self._Ke: np.ndarray        = None
        self._Ni: np.ndarray        = None
        self._d: float              = None
        self._illum: int            = None


        self._map_Kd:  Texture2D    = None
        self._map_Ks: Texture2D     = None
        self._map_Ka: Texture2D     = None
        self._map_Ns: Texture2D     = None
        self._map_Bump: Texture2D   = None
        self._map_d: Texture2D      = None
        
        self._name: str = None
        

        self._type_func: dict[str: function] = {
            # MATERIALS
            "Ns": self.Add_float,
            "Ka": self.Add_vec3,
            "Kd": self.Add_vec3,
            "Ks": self.Add_vec3,
            "Ke": self.Add_vec3,
            "Ni": self.Add_float,
            "d" : self.Add_float,
            "illum": self.Add_int,
            # TEXTURE MAPS
            "map_Kd": self.Add_texture_map,
            "map_Ns": self.Add_texture_map,
            "map_Bump": self.Add_texture_map,
            "map_Ks": self.Add_texture_map,
            "map_d": self.Add_texture_map,
        }
        self._type_prefix_var: dict[str: any] = {}

        self._material_array = np.zeros(len(MATERIAL_SLOT), dtype = object)

    def Add_vec3(self, stride: list[str]):
        prefix = stride[0]
        index = self._PREFIX_TO_SLOT_INDEX[prefix]
        self._material_array[index] = np.array([float(stride[1]), float(stride[2]), float(stride[3])], dtype = np.float32)
    
    def Add_float(self, stride: list[str]):
        prefix = stride[0]
        index = self._PREFIX_TO_SLOT_INDEX[prefix]
        self._material_array[index] = float(stride[1])

    def Add_int(self, stride: list[str]):
        prefix = stride[0]
        index = self._PREFIX_TO_SLOT_INDEX[prefix]
        self._material_array[index] = int(stride[1])

    def Add_texture_map(self, stride: list[str]):
        # return
        
        prefix = stride[0]
        directory = stride[1]
        
        is_exist = os.path.exists(directory)
        if is_exist:
            
            texture = Texture2D(directory)
            texture.Construct()
            index = self._PREFIX_TO_SLOT_INDEX[prefix]
            self._material_array[index] = texture
        else:
            # print(f"WARNING: TEXTURE NOT FOUND ({directory}) -> {prefix}")
            pass



    def Add(self, stride):
        prefix = stride[0]
        method = self._type_func[prefix]
        return method(stride)


    def Fetch(self, prefix: MATERIAL_SLOT, fall_back_value: any = None):
        retreive = self._material_array[prefix]
        if retreive is None:
            return fall_back_value
        return retreive
    

class MaterialManager:
    def __init__(self):
        self._dict_name_mtl: dict[str: Material] = {}
        self._binding_mtl: Material = None
        self._filled: bool = False
    
        self._name: str = None

    def BindMaterial(self, name):
        if not (name in self._dict_name_mtl):
            self._dict_name_mtl[name] = Material()

        self._binding_mtl = self._dict_name_mtl[name]

    def ReadMaterialFile(self, mtl_directory):
        with open(mtl_directory, "r") as f:
            script = f.read().split("\n")
        
        for str_stride in script:
            stride = str_stride.split(" ")
            
            # blank row
            if not stride[0]:
                continue
            
            # comments
            elif stride[0] == "#":
                continue

            prefix = stride[0]

            if prefix == "newmtl":
                name = stride[1]
                self.BindMaterial(name)
                self._binding_mtl._name = name

            else:
                self._binding_mtl.Add(stride)

        f.close()
        self._filled = True

    