"""
This provides gradients to DART, with an eye on embedding DART as a non-linearity in neural networks.
"""
from __future__ import annotations
import _nimblephysics.dynamics
import _nimblephysics.performance
import _nimblephysics.simulation
import collections.abc
import numpy
import numpy.typing
import typing
__all__: list[str] = ['BackpropSnapshot', 'COM', 'COM_POS', 'COM_VEL_LINEAR', 'COM_VEL_SPATIAL', 'ConvertToSpace', 'IKMapping', 'INERTIA_DIAGONAL', 'INERTIA_FULL', 'INERTIA_OFF_DIAGONAL', 'IdentityMapping', 'KnotJacobian', 'LossGradient', 'LossGradientHighLevelAPI', 'MASS', 'MappedBackpropSnapshot', 'Mapping', 'POS_LINEAR', 'POS_SPATIAL', 'VEL_LINEAR', 'VEL_SPATIAL', 'WRT_ACCELERATION', 'WRT_FORCE', 'WRT_GROUP_INERTIAS', 'WRT_GROUP_MASSES', 'WRT_GROUP_SCALES', 'WRT_LINEARIZED_MASSES', 'WRT_POSITION', 'WRT_VELOCITY', 'WithRespectTo', 'WithRespectToAcceleration', 'WithRespectToForce', 'WithRespectToGroupCOMs', 'WithRespectToGroupInertias', 'WithRespectToGroupMasses', 'WithRespectToGroupScales', 'WithRespectToLinearizedMasses', 'WithRespectToMass', 'WithRespectToPosition', 'WithRespectToVelocity', 'WrtMassBodyNodeEntryType', 'WrtMassBodyNodyEntry', 'convertJointSpaceToWorldSpace', 'forwardPass', 'mappedForwardPass']
class BackpropSnapshot:
    def __init__(self, world: _nimblephysics.simulation.World, preStepPosition: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], preStepVelocity: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], preStepTorques: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], preConstraintVelocities: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], preStepLCPCache: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    def backprop(self, world: _nimblephysics.simulation.World, thisTimestepLoss: LossGradient, nextTimestepLoss: LossGradient, perfLog: _nimblephysics.performance.PerformanceLog = None, exploreAlternateStrategies: bool = False) -> None:
        ...
    def backpropState(self, world: _nimblephysics.simulation.World, nextTimestepStateLossGrad: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], perfLog: _nimblephysics.performance.PerformanceLog = None, exploreAlternateStrategies: bool = False) -> LossGradientHighLevelAPI:
        ...
    def benchmarkJacobians(self, world: _nimblephysics.simulation.World, numSamples: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def finiteDifferenceForceVelJacobian(self, world: _nimblephysics.simulation.World, useRidders: bool = True) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def finiteDifferencePosPosJacobian(self, world: _nimblephysics.simulation.World, subdivisions: typing.SupportsInt | typing.SupportsIndex, useRidders: bool = True) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def finiteDifferenceVelPosJacobian(self, world: _nimblephysics.simulation.World, subdivisions: typing.SupportsInt | typing.SupportsIndex, useRidders: bool = True) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def finiteDifferenceVelVelJacobian(self, world: _nimblephysics.simulation.World, useRidders: bool = True) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getActionJacobian(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getControlForceVelJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getInvMassMatrix(self, arg0: _nimblephysics.simulation.World, arg1: bool) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getMassMatrix(self, arg0: _nimblephysics.simulation.World, arg1: bool) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getMassVelJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getPosPosJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getPosVelJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getPostStepPosition(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPostStepTorques(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPostStepVelocity(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPreStepPosition(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPreStepTorques(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPreStepVelocity(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getStateJacobian(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getVelPosJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getVelVelJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
class ConvertToSpace:
    """
    Members:
    
      COM_POS
    
      COM_VEL_LINEAR
    
      COM_VEL_SPATIAL
    
      VEL_LINEAR
    
      VEL_SPATIAL
    
      POS_LINEAR
    
      POS_SPATIAL
    """
    COM_POS: typing.ClassVar[ConvertToSpace]  # value = <ConvertToSpace.COM_POS: 4>
    COM_VEL_LINEAR: typing.ClassVar[ConvertToSpace]  # value = <ConvertToSpace.COM_VEL_LINEAR: 6>
    COM_VEL_SPATIAL: typing.ClassVar[ConvertToSpace]  # value = <ConvertToSpace.COM_VEL_SPATIAL: 5>
    POS_LINEAR: typing.ClassVar[ConvertToSpace]  # value = <ConvertToSpace.POS_LINEAR: 1>
    POS_SPATIAL: typing.ClassVar[ConvertToSpace]  # value = <ConvertToSpace.POS_SPATIAL: 0>
    VEL_LINEAR: typing.ClassVar[ConvertToSpace]  # value = <ConvertToSpace.VEL_LINEAR: 3>
    VEL_SPATIAL: typing.ClassVar[ConvertToSpace]  # value = <ConvertToSpace.VEL_SPATIAL: 2>
    __members__: typing.ClassVar[dict[str, ConvertToSpace]]  # value = {'COM_POS': <ConvertToSpace.COM_POS: 4>, 'COM_VEL_LINEAR': <ConvertToSpace.COM_VEL_LINEAR: 6>, 'COM_VEL_SPATIAL': <ConvertToSpace.COM_VEL_SPATIAL: 5>, 'VEL_LINEAR': <ConvertToSpace.VEL_LINEAR: 3>, 'VEL_SPATIAL': <ConvertToSpace.VEL_SPATIAL: 2>, 'POS_LINEAR': <ConvertToSpace.POS_LINEAR: 1>, 'POS_SPATIAL': <ConvertToSpace.POS_SPATIAL: 0>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class IKMapping(Mapping):
    def __init__(self, arg0: _nimblephysics.simulation.World) -> None:
        ...
    def addAngularBodyNode(self, arg0: _nimblephysics.dynamics.BodyNode) -> None:
        """
        This adds the angular (3D) coordinates of a body node to the mapping, increasing the dimension of the mapped space by 3
        """
    def addLinearBodyNode(self, arg0: _nimblephysics.dynamics.BodyNode) -> None:
        """
        This adds the linear (3D) coordinates of a body node to the mapping, increasing the dimension of the mapped space by 3
        """
    def addSpatialBodyNode(self, arg0: _nimblephysics.dynamics.BodyNode) -> None:
        """
        This adds the spatial (6D) coordinates of a body node to the mapping, increasing the dimension of the mapped space by 6
        """
class IdentityMapping(Mapping):
    def __init__(self, arg0: _nimblephysics.simulation.World) -> None:
        ...
class KnotJacobian:
    def __init__(self) -> None:
        ...
    @property
    def knotPosEndPos(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @knotPosEndPos.setter
    def knotPosEndPos(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def knotPosEndVel(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @knotPosEndVel.setter
    def knotPosEndVel(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def knotVelEndPos(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @knotVelEndPos.setter
    def knotVelEndPos(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def knotVelEndVel(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @knotVelEndVel.setter
    def knotVelEndVel(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def torquesEndPos(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]]:
        ...
    @torquesEndPos.setter
    def torquesEndPos(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> None:
        ...
    @property
    def torquesEndVel(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]]:
        ...
    @torquesEndVel.setter
    def torquesEndVel(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> None:
        ...
class LossGradient:
    def __init__(self) -> None:
        ...
    @property
    def lossWrtPosition(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @lossWrtPosition.setter
    def lossWrtPosition(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def lossWrtTorque(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @lossWrtTorque.setter
    def lossWrtTorque(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def lossWrtVelocity(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @lossWrtVelocity.setter
    def lossWrtVelocity(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
class LossGradientHighLevelAPI:
    def __init__(self) -> None:
        ...
    @property
    def lossWrtAction(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @lossWrtAction.setter
    def lossWrtAction(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def lossWrtMass(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @lossWrtMass.setter
    def lossWrtMass(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def lossWrtState(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @lossWrtState.setter
    def lossWrtState(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
class MappedBackpropSnapshot:
    def backprop(self, world: _nimblephysics.simulation.World, thisTimestepLoss: LossGradient, nextTimestepLosses: collections.abc.Mapping[str, LossGradient], perfLog: _nimblephysics.performance.PerformanceLog = None, exploreAlternateStrategies: bool = False) -> None:
        ...
    def getControlForceMappedVelJacobian(self, world: _nimblephysics.simulation.World, mapAfter: str = 'identity', perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getControlForceVelJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getMappings(self) -> list[str]:
        ...
    def getMassMappedVelJacobian(self, world: _nimblephysics.simulation.World, mapAfter: str = 'identity', perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getMassVelJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getPosMappedPosJacobian(self, world: _nimblephysics.simulation.World, mapAfter: str = 'identity', perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getPosMappedVelJacobian(self, world: _nimblephysics.simulation.World, mapAfter: str = 'identity', perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getPosPosJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getPosVelJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getPostStepPosition(self, mapping: str = 'identity') -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPostStepVelocity(self, mapping: str = 'identity') -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPreStepPosition(self, mapping: str = 'identity') -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPreStepTorques(self, mapping: str = 'identity') -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPreStepVelocity(self, mapping: str = 'identity') -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getVelMappedPosJacobian(self, world: _nimblephysics.simulation.World, mapAfter: str = 'identity', perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getVelMappedVelJacobian(self, world: _nimblephysics.simulation.World, mapAfter: str = 'identity', perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getVelPosJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getVelVelJacobian(self, world: _nimblephysics.simulation.World, perfLog: _nimblephysics.performance.PerformanceLog = None) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
class Mapping:
    def getControlForceDim(self) -> int:
        """
        Gets the dimension of the Force space in this mapping. This will be the length of the getControlForces() vector, and the length of the vector expected by setControlForces().
        """
    def getControlForceLowerLimits(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getControlForceUpperLimits(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getControlForces(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPosDim(self) -> int:
        """
        Gets the dimension of the Position space in this mapping. This will be the length of the getPositions() vector, and the length of the vector expected by setPositions().
        """
    def getPositionLowerLimits(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPositionUpperLimits(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getPositions(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getRealForceToMappedForceJac(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        """
        This returns a Jacobian that transforms the rate of change of the force in the 'real' space given by the world to the rate of change of the force in mapped space.
        """
    def getRealPosToMappedPosJac(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        """
        This returns a Jacobian that transforms the rate of change of the position in the 'real' space given by the world to the rate of change of the position in mapped space.
        """
    def getRealPosToMappedVelJac(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        """
        This returns a Jacobian that transforms the rate of change of the position in the 'real' space given by the world to the rate of change of the velocity in mapped space.
        """
    def getRealVelToMappedPosJac(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        """
        This returns a Jacobian that transforms the rate of change of the velocity in the 'real' space given by the world to the rate of change of the position in mapped space.
        """
    def getRealVelToMappedVelJac(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        """
        This returns a Jacobian that transforms the rate of change of the velocity in the 'real' space given by the world to the rate of change of the velocity in mapped space.
        """
    def getVelDim(self) -> int:
        """
        Gets the dimension of the Velocity space in this mapping. This will be the length of the getVelocities() vector, and the length of the vector expected by setVelocities().
        """
    def getVelocities(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getVelocityLowerLimits(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getVelocityUpperLimits(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def setControlForces(self, world: _nimblephysics.simulation.World, forces: typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]", "flags.writeable"]) -> None:
        ...
    def setMasses(self, world: _nimblephysics.simulation.World, masses: typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]", "flags.writeable"]) -> None:
        ...
    def setPositions(self, world: _nimblephysics.simulation.World, positions: typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]", "flags.writeable"]) -> None:
        ...
    def setVelocities(self, world: _nimblephysics.simulation.World, velocities: typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]", "flags.writeable"]) -> None:
        ...
class WithRespectTo:
    @typing.overload
    def dim(self, world: _nimblephysics.simulation.World) -> int:
        ...
    @typing.overload
    def dim(self, skel: _nimblephysics.dynamics.Skeleton) -> int:
        ...
    @typing.overload
    def get(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @typing.overload
    def get(self, skel: _nimblephysics.dynamics.Skeleton) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def lowerBound(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def name(self) -> str:
        ...
    @typing.overload
    def set(self, world: _nimblephysics.simulation.World, value: typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]) -> None:
        ...
    @typing.overload
    def set(self, skel: _nimblephysics.dynamics.Skeleton, value: typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]) -> None:
        ...
    def upperBound(self, world: _nimblephysics.simulation.World) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
class WithRespectToAcceleration(WithRespectTo):
    pass
class WithRespectToForce(WithRespectTo):
    pass
class WithRespectToGroupCOMs(WithRespectTo):
    pass
class WithRespectToGroupInertias(WithRespectTo):
    pass
class WithRespectToGroupMasses(WithRespectTo):
    pass
class WithRespectToGroupScales(WithRespectTo):
    pass
class WithRespectToLinearizedMasses(WithRespectTo):
    pass
class WithRespectToMass:
    def registerNode(self, node: _nimblephysics.dynamics.BodyNode, type: WrtMassBodyNodeEntryType, upperBound: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], lowerBound: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> WrtMassBodyNodyEntry:
        ...
class WithRespectToPosition(WithRespectTo):
    pass
class WithRespectToVelocity(WithRespectTo):
    pass
class WrtMassBodyNodeEntryType:
    """
    Members:
    
      MASS
    
      COM
    
      INERTIA_DIAGONAL
    
      INERTIA_OFF_DIAGONAL
    
      INERTIA_FULL
    """
    COM: typing.ClassVar[WrtMassBodyNodeEntryType]  # value = <WrtMassBodyNodeEntryType.COM: 1>
    INERTIA_DIAGONAL: typing.ClassVar[WrtMassBodyNodeEntryType]  # value = <WrtMassBodyNodeEntryType.INERTIA_DIAGONAL: 3>
    INERTIA_FULL: typing.ClassVar[WrtMassBodyNodeEntryType]  # value = <WrtMassBodyNodeEntryType.INERTIA_FULL: 5>
    INERTIA_OFF_DIAGONAL: typing.ClassVar[WrtMassBodyNodeEntryType]  # value = <WrtMassBodyNodeEntryType.INERTIA_OFF_DIAGONAL: 4>
    MASS: typing.ClassVar[WrtMassBodyNodeEntryType]  # value = <WrtMassBodyNodeEntryType.MASS: 0>
    __members__: typing.ClassVar[dict[str, WrtMassBodyNodeEntryType]]  # value = {'MASS': <WrtMassBodyNodeEntryType.MASS: 0>, 'COM': <WrtMassBodyNodeEntryType.COM: 1>, 'INERTIA_DIAGONAL': <WrtMassBodyNodeEntryType.INERTIA_DIAGONAL: 3>, 'INERTIA_OFF_DIAGONAL': <WrtMassBodyNodeEntryType.INERTIA_OFF_DIAGONAL: 4>, 'INERTIA_FULL': <WrtMassBodyNodeEntryType.INERTIA_FULL: 5>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class WrtMassBodyNodyEntry:
    linkName: str
    type: WrtMassBodyNodeEntryType
    def __init__(self, arg0: str, arg1: WrtMassBodyNodeEntryType) -> None:
        ...
def convertJointSpaceToWorldSpace(world: _nimblephysics.simulation.World, jointSpace: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], nodes: collections.abc.Sequence[_nimblephysics.dynamics.BodyNode], space: ConvertToSpace, backprop: bool = False, useIK: bool = True) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
    """
    Convert a set of joint positions to a vector of body positions in world space (expressed in log space).
    """
def forwardPass(world: _nimblephysics.simulation.World, idempotent: bool = False) -> BackpropSnapshot:
    ...
def mappedForwardPass(world: _nimblephysics.simulation.World, mappings: collections.abc.Mapping[str, Mapping], idempotent: bool = False) -> MappedBackpropSnapshot:
    ...
COM: WrtMassBodyNodeEntryType  # value = <WrtMassBodyNodeEntryType.COM: 1>
COM_POS: ConvertToSpace  # value = <ConvertToSpace.COM_POS: 4>
COM_VEL_LINEAR: ConvertToSpace  # value = <ConvertToSpace.COM_VEL_LINEAR: 6>
COM_VEL_SPATIAL: ConvertToSpace  # value = <ConvertToSpace.COM_VEL_SPATIAL: 5>
INERTIA_DIAGONAL: WrtMassBodyNodeEntryType  # value = <WrtMassBodyNodeEntryType.INERTIA_DIAGONAL: 3>
INERTIA_FULL: WrtMassBodyNodeEntryType  # value = <WrtMassBodyNodeEntryType.INERTIA_FULL: 5>
INERTIA_OFF_DIAGONAL: WrtMassBodyNodeEntryType  # value = <WrtMassBodyNodeEntryType.INERTIA_OFF_DIAGONAL: 4>
MASS: WrtMassBodyNodeEntryType  # value = <WrtMassBodyNodeEntryType.MASS: 0>
POS_LINEAR: ConvertToSpace  # value = <ConvertToSpace.POS_LINEAR: 1>
POS_SPATIAL: ConvertToSpace  # value = <ConvertToSpace.POS_SPATIAL: 0>
VEL_LINEAR: ConvertToSpace  # value = <ConvertToSpace.VEL_LINEAR: 3>
VEL_SPATIAL: ConvertToSpace  # value = <ConvertToSpace.VEL_SPATIAL: 2>
WRT_ACCELERATION: WithRespectToAcceleration  # value = <_nimblephysics.neural.WithRespectToAcceleration object>
WRT_FORCE: WithRespectToForce  # value = <_nimblephysics.neural.WithRespectToForce object>
WRT_GROUP_INERTIAS: WithRespectToGroupInertias  # value = <_nimblephysics.neural.WithRespectToGroupInertias object>
WRT_GROUP_MASSES: WithRespectToGroupMasses  # value = <_nimblephysics.neural.WithRespectToGroupMasses object>
WRT_GROUP_SCALES: WithRespectToGroupScales  # value = <_nimblephysics.neural.WithRespectToGroupScales object>
WRT_LINEARIZED_MASSES: WithRespectToLinearizedMasses  # value = <_nimblephysics.neural.WithRespectToLinearizedMasses object>
WRT_POSITION: WithRespectToPosition  # value = <_nimblephysics.neural.WithRespectToPosition object>
WRT_VELOCITY: WithRespectToVelocity  # value = <_nimblephysics.neural.WithRespectToVelocity object>
