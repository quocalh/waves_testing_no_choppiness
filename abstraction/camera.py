import numpy as np
import pygame as pg
from pygame.locals import *
from numpy import cos, sin

from components.settings import *

class Projection:
    def __init__(self):
        self._POV_half = np.radians(45)
        

class Camera:
    __slots__ = (
        "_pos", "_orientation", "_world_normal",
        "_sensitivity", "_is_not_1st_held", "_pitch", "_roll", "_roll_clamp",
        "_fov_y", "_aspect", "_near", "_far", "_proj_mat", 
        "_velocity", "_velocity_mult",
    )

    def __init__(self, fov_y =  np.radians(90), aspect = WIDTH / HEIGHT, near = 0.1, far = 100, sensitivity = 0.75):
        self._pos = np.array([0, 0, -4], dtype = np.float32)
        self._orientation = np.array([0, 0, 1], dtype = np.float32)
        self._world_normal = np.array([0, 1, 0], dtype = np.float32)

        self._sensitivity = sensitivity
        self._is_not_1st_held = False
        self._pitch = 0
        self._roll = 0
        self._roll_clamp = np.radians(89)
        
        self._fov_y = fov_y
        self._aspect = aspect
        self._near = near
        self._far = far
        self._proj_mat = self.Perspective

        
        self._velocity = 5
        self._velocity_mult = 2

    @property
    def get_right(self):
        cross = np.cross(self._world_normal, self._orientation)
        return cross  / np.linalg.norm(cross)

    @property
    def get_orientation(self):
        # bruh, i used rotation matrix, could never have thought of such simplicity.

        # note: rotation matrix should be applied on a whole crafted matrix, not a single vector (orientation) since it casually discards rotating inertia 
        
        r = self._roll
        p = self._pitch
        self._orientation[0] = cos(r) * sin(p)
        self._orientation[1] = sin(r)
        self._orientation[2] = cos(r) * cos(p)
        return self._orientation

    @property
    def get_view_mat_real(self):
        # reconstruct the new orientation, right, up (based on the spherical coordinate system)
        self.get_orientation
        o = self._orientation
        r = self.get_right
        u = np.cross(o, r)

        # create a view from previously computed axes (extrinsic rotation matrix - viewed from the origin of the coordinate system)
        # no more flipeed z-axis
        view_mat = np.array([
            [r[0], u[0], o[0],  0   ],
            [r[1], u[1], o[1],  0   ],
            [r[2], u[2], o[2],  0   ],
            [ 0  ,  0  ,  0  ,   1   ],
        ], dtype = np.float32)
        return view_mat

    @property
    def get_view_mat(self):
        # reconstruct the new orientation, right, up (based on the spherical coordinate system)
        self.get_orientation
        o = self._orientation
        r = self.get_right
        u = np.cross(o, r)

        # create a view from previously computed axes (extrinsic rotation matrix - viewed from the origin of the coordinate system)
        
        # note: for some reasons the z_axis must be flipped, in order for OpenGL to work correctly
        view_mat = np.array([
            [r[0], u[0], o[0],   0   ],
            [r[1], u[1], o[1],   0   ],
            [r[2], u[2], o[2],   0   ],
            [ 0  ,  0  ,  0  ,   1   ],
        ], dtype = np.float32)

        return view_mat
        return inverse_z_mat @ view_mat


    def MouseInput(self, dt: float):
        # only used to make changes to _yaw and _pitch -> for reconstructing the orientation, view matrix every loop
        mouse = pg.mouse.get_rel()
        maus_is_held = pg.mouse.get_pressed()[0]

        if maus_is_held:
            # this single line ensures the mouse movement is continuous
            pg.event.set_grab(True)

            pg.mouse.set_visible(False)

            if self._is_not_1st_held == True: # has been holding for a while (not the first time)
                self._pitch += mouse[0] * self._sensitivity * dt
                # the pyame y_axis is inverted, move up (positve rel - but negative input and likewise => flip it)
                self._roll -= mouse[1] * self._sensitivity * dt
            
            
            # clamp the pitch_rotation, i created this concerning that it would cause a reference problem if i just straight up determine self._pitch = +- self._pitch_clamp
            a = self._roll_clamp 
            if self._roll > a:
                self._roll = a
            elif self._roll < -a:
                self._roll = -a

            self.get_orientation
            self._is_not_1st_held = True

        # if mouse is not held
        else:
            pg.event.set_grab(False)
            if self._is_not_1st_held == True:
                pg.mouse.set_pos((WIDTH / 2, HEIGHT / 2))
            self._is_not_1st_held = False
            pg.mouse.set_visible(True)
    
    def KeyInput(self, dt: float):
        velocity_mult = 1
        o = self._orientation
        r = self.get_right
        n = self._world_normal
        v = self._velocity
        
        keys = pg.key.get_pressed()
        if keys[K_LSHIFT]:
            velocity_mult = self._velocity_mult
        if keys[K_w]:
            self._pos += o * velocity_mult * v * dt
        if keys[K_s]:
            self._pos -= o * velocity_mult * v * dt
        if keys[K_d]:
            self._pos += r * velocity_mult * v * dt
        if keys[K_a]:
            self._pos -= r * velocity_mult * v * dt
        if keys[K_SPACE]:
            self._pos += n * velocity_mult * v * dt
        if keys[K_LCTRL]:
            self._pos -= n * velocity_mult * v * dt
    
    @property
    def Perspective(self):
        # the Perspective matrix that i have already done in the previous project
        # I snatched this one on the internet since I know too damn well why it works, and how can i reconstruct it from scratch
        f = 1.0 / np.tan(self._fov_y / 2.0)
        depth = self._near - self._far
        proj = np.array([
            [f / self._aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (self._far + self._near) / depth, (2 * self._far * self._near) / depth],
            [0, 0, -1, 0]
        ], dtype = np.float32)

        return proj
    
    def SetPerspective(self, new_fov_y):
        self._fov_y = new_fov_y
        self._proj_mat = self.Perspective
        
    
    @property
    def GetTransformationMat(self):
        # note, calling it intrinsic is just misleading, since we deploy the mat with no interest in twisting the whole reference frame
        # after all, transpose mattrix doesn't flip the rotation order (it does but comes with inverted in angles), but give an opposite rotation (desired result)
        # to be precise, what we are doing - i would only call it perspective transformation
            # which means translating the object in a way that relative to the camera
                # and then apply inverse rotation (if you look to the right, mathematically and intuitively, the world will rotate to the left)
            # so to see the world in the perspective of the camera 
                # -> given P (world coord random points), Q (camera's position) belong to R^3 and M (view mat of the camera):
             # P_in_perspective = (P - Q) * M^(-1) // translate first, inverse rotate later (with orthogonality it can be either a transpose or an inverse) 

        
        inverse_z_mat = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0,-1, 0],
            [0, 0, 0, 1],
        ])
        # world space perspective (rotate then translate)
        # NOTE: (view_mat * inversez)^T = inversez^T * view_mat^T
        return self._proj_mat @ (inverse_z_mat.T @ self.get_view_mat.T)  @ self.Translate(-self._pos)
        return (self._proj_mat @ inverse_z_mat.T) @ self.get_view_mat.T @ self.Translate(-self._pos)


    
    @staticmethod
    def Translate(value: np.ndarray):
        return np.array([
            [1, 0, 0, value[0]],
            [0, 1, 0, value[1]],
            [0, 0, 1, value[2]],
            [0, 0, 0,    1    ],
        ], dtype = np.float32)
    


