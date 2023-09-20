"""
A pygame based 3D graphics library.
"""

# Imports
from __future__ import annotations
import pygame
import math
import os


class Entity:
    def __init__(self):
        self.parent = None
        self.children = []

        self._position = pygame.Vector3(0, 0, 0)
        self._orientation = pygame.Vector3(0, 0, 0)
        self._scale = pygame.Vector3(1, 1, 1)

        self._global_position = self._position
        self._global_orientation = self._orientation
        self._global_scale = self._scale

    def _recalculate(self):
        if self.parent is not None:
            # TODO: rotations
            self._global_position = self.parent._global_position + self._position
            self._global_orientation = (
                self.parent._global_orientation + self._orientation
            )
            self._global_scale = self.parent._global_scale * self._scale

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
        # [
        #     [
        #         ((x, y, z), (u, v), (normal)),
        #     ],
        # ]
        self._global_mesh = self.mesh

    def _recalculate(self):
        Entity._recalculate(self)

        self._global_mesh = self.mesh
        for face in self._global_mesh:
            for vertex in face:
                vertex[0] = vertex[0] + self._global_position

    def from_file(path: os.PathLike | str):
        """
        .obj loader
        """
        mesh = Mesh()

        vertices = []
        uvs = []
        normals = []

        with open(path, "r") as file:
            for line in file.readlines():
                if line.startswith("v "):
                    # Vertex
                    x, y, z = line[2:].split(" ")
                    vertices.append(
                        pygame.Vector3(float(x) * 50, -float(y) * 50, float(z) * 50)
                    )

                elif line.startswith("vt "):
                    # UV
                    u, v = line[3:].split(" ")[:-1]
                    uvs.append((float(u), float(v)))

                elif line.startswith("vn "):
                    # Normal
                    x, y, z = line[3:].split(" ")
                    normals.append((float(x), float(y), float(z)))

                elif line.startswith("f "):
                    # Face
                    indices = [
                        [int(i) for i in element.split("/")]
                        for element in line[2:].split(" ")
                    ]

                    face = []
                    for index in indices:
                        if len(index) == 1:
                            face.append([vertices[index[0] - 1], None, None])
                        elif len(index) == 2:
                            face.append(
                                [vertices[index[0] - 1], uvs[index[1] - 1], None]
                            )
                        elif len(index) == 3:
                            face.append(
                                [
                                    vertices[index[0] - 1],
                                    uvs[index[1] - 1],
                                    normals[index[2] - 1],
                                ]
                            )

                    mesh.mesh.append(face)

        return mesh


class Camera(Entity):
    def __init__(self, scene: Scene):
        self.scene = scene
        self.fov = 90

    def render(self, screen: pygame.Surface):
        x_focal_length = screen.get_width() / (2 * math.tan(math.radians(self.fov / 2)))
        y_focal_length = screen.get_height() / (
            2 * math.tan(math.radians(self.fov / 2))
        )

        # TODO: render
        screen.fill("white")  # TODO: skybox???

        for child in self.scene.children:
            for face in child._global_mesh:
                pygame.draw.polygon(
                    screen,
                    "black",
                    [
                        pygame.Vector2(
                            (i[0][0] * x_focal_length) / (i[0][2] + x_focal_length),
                            i[0][1] * y_focal_length / (i[0][2] + y_focal_length),
                        )
                        + (screen.get_width() / 2, screen.get_height() / 2)
                        for i in face
                    ],
                )


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

        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.camera.render(screen)

            pygame.display.flip()
            clock.tick(60)
