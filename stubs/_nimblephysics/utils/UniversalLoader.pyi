from __future__ import annotations
import _nimblephysics.dynamics
import _nimblephysics.simulation
import numpy
import numpy.typing
import typing
__all__: list[str] = ['loadMeshShape', 'loadSkeleton', 'loadWorld']
def loadMeshShape(path: str) -> _nimblephysics.dynamics.MeshShape:
    ...
def loadSkeleton(world: _nimblephysics.simulation.World, path: str, basePosition: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], baseEulerXYZ: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> _nimblephysics.dynamics.Skeleton:
    ...
def loadWorld(path: str) -> _nimblephysics.simulation.World:
    ...
