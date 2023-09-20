"""
A pygame based 3D graphics library.
"""

# Imports
import pygame
import math
import os


class Entity:
    def __init__(self):
        self.parent = None
        self.children = []

        self.position = pygame.Vector3(0, 0, 0)
        self.orientation = pygame.Vector3(0, 0, 0)
        self.scale = pygame.Vector3(1, 1, 1)

        self._global_position = self.position
        self._global_orientation = self.orientation
        self._global_scale = self.scale

    def _recalculate(self):
        if self.parent is not None:
            # TODO: rotations
            self._global_position = self.parent._global_position + self.position
            self._global_orientation = (
                self.parent._global_orientation + self.orientation
            )
            self._global_scale = self.parent._global_scale * self.scale

        # Recalculate children
        for child in self.children:
            child._recalculate()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = pygame.Vector3(value)
        self._recalculate()

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = pygame.Vector3(value)
        self._recalculate()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = pygame.Vector3(value)
        self._recalculate()


class Mesh(Entity):
    def __init__(self):
        """
        Do not call directly. Use `.from_file` to load a mesh from a file. Other loading methods are on the way.
        """
        Entity.__init__(self)
        self.mesh = []

    def from_file(path: os.PathLike | str):
        """
        .obj loader
        """
        mesh = Mesh()
        # mesh.mesh = ?????
        return mesh


class Camera(Entity):
    def __init__(self, scene: Scene):
        self.scene = scene

    def render(self, screen: pygame.Surface):
        # TODO: render
        screen.fill("white")  # TODO: skybox???


class Scene(Entity):
    def __init__(
        self,
    ):
        Entity.__init__(self)
        self.camera = Camera(self)

    def add(self, child: Entity):
        child.parent = self
        self.children.append(child)

    def run(self):
        screen = pygame.display.set_mode((800, 600))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.camera.render(screen)

            pygame.display.flip()
