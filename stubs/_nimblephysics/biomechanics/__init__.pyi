"""
This provides biomechanics utilities in Nimble, including inverse dynamics and (eventually) mocap support and muscle estimation.
"""
from __future__ import annotations
import _nimblephysics.dynamics
import _nimblephysics.math
import _nimblephysics.neural
import collections.abc
import numpy
import numpy.typing
import typing
from . import OpenSimParser
__all__: list[str] = ['Anthropometrics', 'BasicTrialType', 'BatchGaitInverseDynamics', 'Beam', 'BilevelFitResult', 'C3D', 'C3DLoader', 'ContactRegimeSection', 'CortexStreaming', 'DataQuality', 'DetectedTrialFeature', 'DynamicsFitProblemConfig', 'DynamicsFitter', 'DynamicsInitialization', 'ForcePlate', 'Frame', 'FrameList', 'FramePass', 'FramePassList', 'IKErrorReport', 'IMUFineTuneProblem', 'InitialMarkerFitParams', 'LabelledMarkers', 'LilypadSolver', 'LinkBeam', 'LinkBeamSearch', 'MarkerBeamSearch', 'MarkerFitter', 'MarkerFitterState', 'MarkerFixer', 'MarkerInitialization', 'MarkerLabeller', 'MarkerLabellerMock', 'MarkerMultiBeamSearch', 'MarkerTrace', 'MarkersErrorReport', 'MissingGRFReason', 'MissingGRFStatus', 'MultiBeam', 'NeuralMarkerLabeller', 'OpenSimFile', 'OpenSimMocoTrajectory', 'OpenSimMot', 'OpenSimParser', 'OpenSimScaleAndMarkerOffsets', 'OpenSimTRC', 'ProcessingPassType', 'ResidualForceHelper', 'SkeletonConverter', 'StreamingIK', 'StreamingMarkerTraces', 'StreamingMocapLab', 'SubjectOnDisk', 'SubjectOnDiskHeader', 'SubjectOnDiskPassHeader', 'SubjectOnDiskTrial', 'SubjectOnDiskTrialPass', 'TraceHead', 'copOutsideConvexFootError', 'extendedToNearestPeakForce', 'footContactDetectedButNoForce', 'forceDiscrepancy', 'hasInputOutliers', 'hasNoForcePlateData', 'interpolatedClippedGRF', 'manualReview', 'measuredGrfZeroWhenAccelerationNonZero', 'missingBlip', 'missingImpact', 'no', 'notMissingGRF', 'notOverForcePlate', 'shiftGRF', 'tooHighMarkerRMS', 'torqueDiscrepancy', 'unknown', 'unmeasuredExternalForceDetected', 'velocitiesStillTooHighAfterFiltering', 'yes', 'zeroForceFrame']
class Anthropometrics:
    @staticmethod
    def loadFromFile(uri: str) -> Anthropometrics:
        ...
    def addMetric(self, name: str, bodyPose: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], bodyA: str, offsetA: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], bodyB: str, offsetB: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], axis: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"] = ...) -> None:
        ...
    def condition(self, observedValues: collections.abc.Mapping[str, typing.SupportsFloat | typing.SupportsIndex]) -> Anthropometrics:
        ...
    def debugToGUI(self, server: ..., skel: _nimblephysics.dynamics.Skeleton) -> None:
        ...
    def getDistribution(self) -> _nimblephysics.math.MultivariateGaussian:
        ...
    def getGradientOfLogPDFWrtBodyScales(self, skel: _nimblephysics.dynamics.Skeleton) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getGradientOfLogPDFWrtGroupScales(self, skel: _nimblephysics.dynamics.Skeleton) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getLogPDF(self, skel: _nimblephysics.dynamics.Skeleton, normalized: bool = True) -> float:
        ...
    def getMetricNames(self) -> list[str]:
        ...
    def getPDF(self, skel: _nimblephysics.dynamics.Skeleton) -> float:
        ...
    def measure(self, skel: _nimblephysics.dynamics.Skeleton) -> dict[str, float]:
        ...
    def setDistribution(self, dist: _nimblephysics.math.MultivariateGaussian) -> None:
        ...
class BasicTrialType:
    """
    Members:
    
      TREADMILL : This is a trial where the subject is walking or running on a treadmill.
    
      OVERGROUND : This is a trial where the subject is walking or running overground.
    
      STATIC_TRIAL : This is a trial where the subject is standing still.
    
      OTHER : This is a trial that doesn't fit into any of the other categories.
    """
    OTHER: typing.ClassVar[BasicTrialType]  # value = <BasicTrialType.OTHER: 3>
    OVERGROUND: typing.ClassVar[BasicTrialType]  # value = <BasicTrialType.OVERGROUND: 1>
    STATIC_TRIAL: typing.ClassVar[BasicTrialType]  # value = <BasicTrialType.STATIC_TRIAL: 2>
    TREADMILL: typing.ClassVar[BasicTrialType]  # value = <BasicTrialType.TREADMILL: 0>
    __members__: typing.ClassVar[dict[str, BasicTrialType]]  # value = {'TREADMILL': <BasicTrialType.TREADMILL: 0>, 'OVERGROUND': <BasicTrialType.OVERGROUND: 1>, 'STATIC_TRIAL': <BasicTrialType.STATIC_TRIAL: 2>, 'OTHER': <BasicTrialType.OTHER: 3>}
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
class BatchGaitInverseDynamics:
    def __init__(self, skeleton: _nimblephysics.dynamics.Skeleton, poses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], groundContactBodies: collections.abc.Sequence[_nimblephysics.dynamics.BodyNode], groundNormal: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], tileSize: typing.SupportsFloat | typing.SupportsIndex, maxSectionLength: typing.SupportsInt | typing.SupportsIndex = 100, smoothingWeight: typing.SupportsFloat | typing.SupportsIndex = 1.0, minTorqueWeight: typing.SupportsFloat | typing.SupportsIndex = 1.0, prevContactWeight: typing.SupportsFloat | typing.SupportsIndex = 0.1, blendWeight: typing.SupportsFloat | typing.SupportsIndex = 1.0, blendSteepness: typing.SupportsFloat | typing.SupportsIndex = 10.0) -> None:
        ...
    def debugLilypadToGUI(self, gui: ...) -> None:
        ...
    def debugTimestepToGUI(self, gui: ..., timesteps: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def getContactBodiesAtTimestep(self, timestep: typing.SupportsInt | typing.SupportsIndex) -> list[_nimblephysics.dynamics.BodyNode]:
        ...
    def getContactWrenchesAtTimestep(self, timestep: typing.SupportsInt | typing.SupportsIndex) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[6, 1]"]]:
        ...
    def getSectionForTimestep(self, timestep: typing.SupportsInt | typing.SupportsIndex) -> ContactRegimeSection:
        ...
    def numTimesteps(self) -> int:
        ...
class Beam:
    def __init__(self, label: str, cost: typing.SupportsFloat | typing.SupportsIndex, observed_this_timestep: bool, last_observed_point: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], last_observed_timestamp: typing.SupportsFloat | typing.SupportsIndex, last_observed_velocity: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], parent: Beam) -> None:
        ...
    @property
    def cost(self) -> float:
        ...
    @property
    def label(self) -> str:
        ...
    @property
    def last_observed_point(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        ...
    @property
    def last_observed_timestamp(self) -> float:
        ...
    @property
    def last_observed_velocity(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        ...
    @property
    def observed_this_timestep(self) -> bool:
        ...
    @property
    def parent(self) -> Beam:
        ...
class BilevelFitResult:
    success: bool
    @property
    def groupScales(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @groupScales.setter
    def groupScales(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def markerOffsets(self) -> dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @markerOffsets.setter
    def markerOffsets(self, arg0: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def poses(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]]:
        ...
    @poses.setter
    def poses(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]]) -> None:
        ...
    @property
    def posesMatrix(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @posesMatrix.setter
    def posesMatrix(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def rawMarkerOffsets(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @rawMarkerOffsets.setter
    def rawMarkerOffsets(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
class C3D:
    @property
    def dataRotation(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 3]"]:
        ...
    @dataRotation.setter
    def dataRotation(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 3]"]) -> None:
        ...
    @property
    def forcePlates(self) -> list[ForcePlate]:
        ...
    @forcePlates.setter
    def forcePlates(self, arg0: collections.abc.Sequence[ForcePlate]) -> None:
        ...
    @property
    def framesPerSecond(self) -> int:
        ...
    @framesPerSecond.setter
    def framesPerSecond(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def markerTimesteps(self) -> list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @markerTimesteps.setter
    def markerTimesteps(self, arg0: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def markers(self) -> list[str]:
        ...
    @markers.setter
    def markers(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
    @property
    def shuffledMarkersMatrix(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @shuffledMarkersMatrix.setter
    def shuffledMarkersMatrix(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def shuffledMarkersMatrixMask(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @shuffledMarkersMatrixMask.setter
    def shuffledMarkersMatrixMask(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def timestamps(self) -> list[float]:
        ...
    @timestamps.setter
    def timestamps(self, arg0: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
class C3DLoader:
    @staticmethod
    def debugToGUI(file: C3D, server: ...) -> None:
        ...
    @staticmethod
    def fixupMarkerFlips(c3d: C3D) -> list[list[tuple[str, str]]]:
        ...
    @staticmethod
    def loadC3D(uri: str) -> C3D:
        ...
class ContactRegimeSection:
    @property
    def endTime(self) -> int:
        ...
    @endTime.setter
    def endTime(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def groundContactBodies(self) -> list[_nimblephysics.dynamics.BodyNode]:
        ...
    @groundContactBodies.setter
    def groundContactBodies(self, arg0: collections.abc.Sequence[_nimblephysics.dynamics.BodyNode]) -> None:
        ...
    @property
    def startTime(self) -> int:
        ...
    @startTime.setter
    def startTime(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def wrenches(self) -> list[list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[6, 1]"]]]:
        ...
    @wrenches.setter
    def wrenches(self, arg0: collections.abc.Sequence[collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[6, 1]"]]]) -> None:
        ...
class CortexStreaming:
    def __init__(self, cortexNicAddress: str, cortexMulticastPort: typing.SupportsInt | typing.SupportsIndex = 1001, cortexRequestsPort: typing.SupportsInt | typing.SupportsIndex = 1510) -> None:
        ...
    def connect(self) -> None:
        """
        This creates a UDP socket and starts listening for packets from Cortex
        """
    def disconnect(self) -> None:
        """
        This closes the UDP socket and stops listening for packets from Cortex
        """
    def initialize(self) -> None:
        """
        This connects to Cortex, and requests the body defs and a frame of data
        """
    def mockServerSendFrameMulticast(self) -> None:
        """
        This sends a UDP packet out on the multicast address, to tell everyone about the current frame
        """
    def mockServerSetData(self, markerNames: collections.abc.Sequence[str], markers: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]], copTorqueForces: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> None:
        """
        This is used for mocking the Cortex API server for local testing. This sets the current body defs and frame of data to send back to the client.
        """
    def setFrameHandler(self, handler: collections.abc.Callable[[collections.abc.Sequence[str], collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]], collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]], None]) -> None:
        """
        This is the callback that gets called when a frame of data is received
        """
    def startMockServer(self) -> None:
        """
        This starts a UDP server that mimicks the Cortex API, so we can test locally without having to run Cortex. This is an alternative to connect(), and cannot run in the same process as connect().
        """
class DataQuality:
    """
    Members:
    
      PILOT_DATA : This is data that was collected as part of a pilot study.
    
      EXPERIMENTAL_DATA : This is data that was collected as part of an experiment.
    
      INTERNET_DATA : This is data that was collected from the internet.
    """
    EXPERIMENTAL_DATA: typing.ClassVar[DataQuality]  # value = <DataQuality.EXPERIMENTAL_DATA: 1>
    INTERNET_DATA: typing.ClassVar[DataQuality]  # value = <DataQuality.INTERNET_DATA: 2>
    PILOT_DATA: typing.ClassVar[DataQuality]  # value = <DataQuality.PILOT_DATA: 0>
    __members__: typing.ClassVar[dict[str, DataQuality]]  # value = {'PILOT_DATA': <DataQuality.PILOT_DATA: 0>, 'EXPERIMENTAL_DATA': <DataQuality.EXPERIMENTAL_DATA: 1>, 'INTERNET_DATA': <DataQuality.INTERNET_DATA: 2>}
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
class DetectedTrialFeature:
    """
    Members:
    
      WALKING : This is a trial where the subject is walking.
    
      RUNNING : This is a trial where the subject is running.
    
      UNEVEN_TERRAIN : This is a trial where the subject is walking or running on uneven terrain.
    
      FLAT_TERRAIN : This is a trial where the subject is walking or running on flat terrain.
    """
    FLAT_TERRAIN: typing.ClassVar[DetectedTrialFeature]  # value = <DetectedTrialFeature.FLAT_TERRAIN: 3>
    RUNNING: typing.ClassVar[DetectedTrialFeature]  # value = <DetectedTrialFeature.RUNNING: 1>
    UNEVEN_TERRAIN: typing.ClassVar[DetectedTrialFeature]  # value = <DetectedTrialFeature.UNEVEN_TERRAIN: 2>
    WALKING: typing.ClassVar[DetectedTrialFeature]  # value = <DetectedTrialFeature.WALKING: 0>
    __members__: typing.ClassVar[dict[str, DetectedTrialFeature]]  # value = {'WALKING': <DetectedTrialFeature.WALKING: 0>, 'RUNNING': <DetectedTrialFeature.RUNNING: 1>, 'UNEVEN_TERRAIN': <DetectedTrialFeature.UNEVEN_TERRAIN: 2>, 'FLAT_TERRAIN': <DetectedTrialFeature.FLAT_TERRAIN: 3>}
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
class DynamicsFitProblemConfig:
    def __init__(self, skeleton: _nimblephysics.dynamics.Skeleton) -> None:
        ...
    def setBoundMoveDistance(self, distance: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setConstrainAngularResiduals(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setConstrainLinearResiduals(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setConstrainResidualsZero(self, constrain: bool) -> DynamicsFitProblemConfig:
        ...
    def setDefaults(self, useL1: bool = True) -> DynamicsFitProblemConfig:
        ...
    def setDisableBounds(self, disable: bool) -> DynamicsFitProblemConfig:
        ...
    def setIncludeBodyScales(self, value: bool) -> DynamicsFitProblemConfig:
        ...
    def setIncludeCOMs(self, value: bool) -> DynamicsFitProblemConfig:
        ...
    def setIncludeInertias(self, value: bool) -> DynamicsFitProblemConfig:
        ...
    def setIncludeMarkerOffsets(self, value: bool) -> DynamicsFitProblemConfig:
        ...
    def setIncludeMasses(self, value: bool) -> DynamicsFitProblemConfig:
        ...
    def setIncludePoses(self, value: bool) -> DynamicsFitProblemConfig:
        ...
    def setJointWeight(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setLinearNewtonUseL1(self, value: bool) -> DynamicsFitProblemConfig:
        ...
    def setLinearNewtonWeight(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setLogLossDetails(self, value: bool) -> DynamicsFitProblemConfig:
        ...
    def setMarkerUseL1(self, value: bool) -> DynamicsFitProblemConfig:
        ...
    def setMarkerWeight(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setMaxBlockSize(self, value: typing.SupportsInt | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setMaxNumBlocksPerTrial(self, value: typing.SupportsInt | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setMaxNumTrials(self, value: typing.SupportsInt | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setNumThreads(self, value: typing.SupportsInt | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setOnlyOneTrial(self, value: typing.SupportsInt | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setPoseSubsetLen(self, value: typing.SupportsInt | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setPoseSubsetStartIndex(self, value: typing.SupportsInt | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setRegularizeAnatomicalMarkerOffsets(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setRegularizeBodyScales(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setRegularizeCOMs(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setRegularizeImpliedDensity(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setRegularizeInertias(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setRegularizeJointAcc(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setRegularizeMasses(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setRegularizePoses(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setRegularizeSpatialAcc(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setRegularizeSpatialAccBodyWeights(self, bodyWeights: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> DynamicsFitProblemConfig:
        ...
    def setRegularizeSpatialAccUseL1(self, value: bool) -> DynamicsFitProblemConfig:
        ...
    def setRegularizeTrackingMarkerOffsets(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setResidualTorqueMultiple(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
    def setResidualUseL1(self, value: bool) -> DynamicsFitProblemConfig:
        ...
    def setResidualWeight(self, value: typing.SupportsFloat | typing.SupportsIndex) -> DynamicsFitProblemConfig:
        ...
class DynamicsFitter:
    @staticmethod
    @typing.overload
    def createInitialization(skel: _nimblephysics.dynamics.Skeleton, markerMap: collections.abc.Mapping[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], trackingMarkers: collections.abc.Sequence[str], grfNodes: collections.abc.Sequence[_nimblephysics.dynamics.BodyNode], forcePlateTrials: collections.abc.Sequence[collections.abc.Sequence[ForcePlate]], poseTrials: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]], framesPerSecond: collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex], markerObservationTrials: collections.abc.Sequence[collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]], overrideForcePlateToGRFNodeAssignment: collections.abc.Sequence[collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex]] = [], initializedProbablyMissingGRF: collections.abc.Sequence[collections.abc.Sequence[MissingGRFStatus]] = []) -> DynamicsInitialization:
        ...
    @staticmethod
    @typing.overload
    def createInitialization(skel: _nimblephysics.dynamics.Skeleton, kinematicInits: collections.abc.Sequence[MarkerInitialization], trackingMarkers: collections.abc.Sequence[str], grfNodes: collections.abc.Sequence[_nimblephysics.dynamics.BodyNode], forcePlateTrials: collections.abc.Sequence[collections.abc.Sequence[ForcePlate]], framesPerSecond: collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex], markerObservationTrials: collections.abc.Sequence[collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]], overrideForcePlateToGRFNodeAssignment: collections.abc.Sequence[collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex]] = [], initializedProbablyMissingGRF: collections.abc.Sequence[collections.abc.Sequence[MissingGRFStatus]] = []) -> DynamicsInitialization:
        ...
    def __init__(self, skeleton: _nimblephysics.dynamics.Skeleton, footNodes: collections.abc.Sequence[_nimblephysics.dynamics.BodyNode], trackingMarkers: collections.abc.Sequence[str]) -> None:
        ...
    def addJointBoundSlack(self, init: _nimblephysics.dynamics.Skeleton, slack: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def applyInitToSkeleton(self, skel: _nimblephysics.dynamics.Skeleton, init: DynamicsInitialization) -> None:
        ...
    def boundPush(self, init: DynamicsInitialization, boundPush: typing.SupportsFloat | typing.SupportsIndex = 0.02) -> None:
        ...
    def checkPhysicalConsistency(self, init: DynamicsInitialization, maxAcceptableErrors: typing.SupportsFloat | typing.SupportsIndex = 0.001, maxTimestepsToTest: typing.SupportsInt | typing.SupportsIndex = 50) -> bool:
        ...
    def comAccelerations(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    def comPositions(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    def computeAverageCOPChange(self, init: DynamicsInitialization) -> float:
        ...
    def computeAverageForceMagnitudeChange(self, init: DynamicsInitialization) -> float:
        ...
    def computeAverageForceVectorChange(self, init: DynamicsInitialization) -> float:
        ...
    def computeAverageMarkerMaxError(self, init: DynamicsInitialization) -> float:
        ...
    def computeAverageMarkerRMSE(self, init: DynamicsInitialization) -> float:
        ...
    def computeAverageRealForce(self, init: DynamicsInitialization) -> tuple[float, float]:
        ...
    def computeAverageResidualForce(self, init: DynamicsInitialization) -> tuple[float, float]:
        ...
    def computeAverageTrialCOPChange(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex) -> float:
        ...
    def computeAverageTrialForceMagnitudeChange(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex) -> float:
        ...
    def computeAverageTrialForceVectorChange(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex) -> float:
        ...
    def computeAverageTrialMarkerMaxError(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex) -> float:
        ...
    def computeAverageTrialMarkerRMSE(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex) -> float:
        ...
    def computeAverageTrialRealForce(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex) -> tuple[float, float]:
        ...
    def computeAverageTrialResidualForce(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex) -> tuple[float, float]:
        ...
    def computeInverseDynamics(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def computePerfectGRFs(self, init: DynamicsInitialization) -> None:
        ...
    def estimateFootGroundContactsWithHeightHeuristic(self, init: DynamicsInitialization, ignoreFootNotOverForcePlate: bool = False) -> None:
        ...
    def estimateFootGroundContactsWithStillness(self, init: DynamicsInitialization, radius: typing.SupportsFloat | typing.SupportsIndex = 0.05, minTime: typing.SupportsFloat | typing.SupportsIndex = 0.5) -> None:
        ...
    def estimateLinkMassesFromAcceleration(self, init: DynamicsInitialization, regularizationWeight: typing.SupportsFloat | typing.SupportsIndex = 50.0) -> None:
        ...
    def impliedCOMForces(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex, includeGravity: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"] = True) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    def measuredGRFForces(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    def multimassZeroLinearResidualsOnCOMTrajectory(self, init: DynamicsInitialization, maxTrialsToSolveMassOver: typing.SupportsInt | typing.SupportsIndex = 4, boundPush: typing.SupportsFloat | typing.SupportsIndex = 0.01) -> None:
        ...
    def optimizeMarkerOffsets(self, init: DynamicsInitialization, reoptimizeAnatomicalMarkers: bool = False, reoptimizeTrackingMarkers: bool = True) -> None:
        ...
    def optimizeSpatialResidualsOnCOMTrajectory(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex, satisfactoryThreshold: typing.SupportsFloat | typing.SupportsIndex = 1e-05, numIters: typing.SupportsInt | typing.SupportsIndex = 600, missingResidualRegularization: typing.SupportsFloat | typing.SupportsIndex = 1000, weightAngular: typing.SupportsFloat | typing.SupportsIndex = 2.0, weightLastFewTimesteps: typing.SupportsFloat | typing.SupportsIndex = 5.0, offsetRegularization: typing.SupportsFloat | typing.SupportsIndex = 0.001, regularizeResiduals: bool = True) -> bool:
        ...
    def recalibrateForcePlates(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex, maxMovement: typing.SupportsFloat | typing.SupportsIndex = 0.03) -> None:
        ...
    def runConstrainedSGDOptimization(self, init: DynamicsInitialization, config: DynamicsFitProblemConfig) -> None:
        ...
    def runIPOPTOptimization(self, init: DynamicsInitialization, config: DynamicsFitProblemConfig) -> None:
        ...
    def runUnconstrainedSGDOptimization(self, init: DynamicsInitialization, config: DynamicsFitProblemConfig) -> None:
        ...
    def saveDynamicsToGUI(self, path: str, init: DynamicsInitialization, trialIndex: typing.SupportsInt | typing.SupportsIndex, framesPerSecond: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def scaleLinkMassesFromGravity(self, init: DynamicsInitialization) -> None:
        ...
    def setCOMHistogramBuckets(self, buckets: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setCOMHistogramClipBuckets(self, clipBuckets: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setCOMHistogramMaxMovement(self, maxMovement: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setCheckDerivatives(self, value: bool) -> None:
        ...
    def setDisableLinesearch(self, value: bool) -> None:
        ...
    def setFillInEndFramesGrfGaps(self, fillInFrames: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setIterationLimit(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setLBFGSHistoryLength(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setPrintFrequency(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setSilenceOutput(self, value: bool) -> None:
        ...
    def setTolerance(self, value: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def smoothAccelerations(self, init: DynamicsInitialization, smoothingWeight: typing.SupportsFloat | typing.SupportsIndex = 10.0, regularizationWeight: typing.SupportsFloat | typing.SupportsIndex = 0.001) -> None:
        ...
    def timeSyncAndInitializePipeline(self, init: DynamicsInitialization, useReactionWheels: bool = False, shiftGRF: bool = False, maxShiftGRF: typing.SupportsInt | typing.SupportsIndex = 4, iterationsPerShift: typing.SupportsInt | typing.SupportsIndex = 20, maxTrialsToSolveMassOver: typing.SupportsInt | typing.SupportsIndex = 4, weightLinear: typing.SupportsFloat | typing.SupportsIndex = 1.0, weightAngular: typing.SupportsFloat | typing.SupportsIndex = 0.5, regularizeLinearResiduals: typing.SupportsFloat | typing.SupportsIndex = 0.1, regularizeAngularResiduals: typing.SupportsFloat | typing.SupportsIndex = 0.1, regularizeCopDriftCompensation: typing.SupportsFloat | typing.SupportsIndex = 1.0, maxBuckets: typing.SupportsInt | typing.SupportsIndex = 100, detectUnmeasuredTorque: bool = True, avgPositionChangeThreshold: typing.SupportsFloat | typing.SupportsIndex = 0.08, avgAngularChangeThreshold: typing.SupportsFloat | typing.SupportsIndex = 0.15, reoptimizeAnatomicalMarkers: bool = False, reoptimizeTrackingMarkers: bool = True, tuneLinkMasses: bool = False) -> bool:
        ...
    def timeSyncTrialGRF(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex, useReactionWheels: bool = False, maxShiftGRF: typing.SupportsInt | typing.SupportsIndex = 4, iterationsPerShift: typing.SupportsInt | typing.SupportsIndex = 20, weightLinear: typing.SupportsFloat | typing.SupportsIndex = 1.0, weightAngular: typing.SupportsFloat | typing.SupportsIndex = 1.0, regularizeLinearResiduals: typing.SupportsFloat | typing.SupportsIndex = 0.5, regularizeAngularResiduals: typing.SupportsFloat | typing.SupportsIndex = 0.5, regularizeCopDriftCompensation: typing.SupportsFloat | typing.SupportsIndex = 1.0, maxBuckets: typing.SupportsInt | typing.SupportsIndex = 20) -> bool:
        ...
    def writeCSVData(self, path: str, init: DynamicsInitialization, trialIndex: typing.SupportsInt | typing.SupportsIndex, useAdjustedGRFs: bool = False, timestamps: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex] = []) -> None:
        ...
    def zeroLinearResidualsAndOptimizeAngular(self, init: DynamicsInitialization, trial: typing.SupportsInt | typing.SupportsIndex, targetPoses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], previousTotalResidual: typing.SupportsFloat | typing.SupportsIndex, iteration: typing.SupportsInt | typing.SupportsIndex, useReactionWheels: bool = False, weightLinear: typing.SupportsFloat | typing.SupportsIndex = 1.0, weightAngular: typing.SupportsFloat | typing.SupportsIndex = 0.5, regularizeLinearResiduals: typing.SupportsFloat | typing.SupportsIndex = 0.1, regularizeAngularResiduals: typing.SupportsFloat | typing.SupportsIndex = 0.1, regularizeCopDriftCompensation: typing.SupportsFloat | typing.SupportsIndex = 1.0, maxBuckets: typing.SupportsInt | typing.SupportsIndex = 40, maxLeastSquaresIters: typing.SupportsInt | typing.SupportsIndex = 200, commitCopDriftCompensation: bool = False, detectUnmeasuredTorque: bool = True, avgPositionChangeThreshold: typing.SupportsFloat | typing.SupportsIndex = 0.08, avgAngularChangeThreshold: typing.SupportsFloat | typing.SupportsIndex = 0.15) -> tuple[bool, bool, float]:
        ...
    def zeroLinearResidualsOnCOMTrajectory(self, init: DynamicsInitialization, maxTrialsToSolveMassOver: typing.SupportsInt | typing.SupportsIndex = 4, detectExternalForce: bool = True, driftCorrectionBlurRadius: typing.SupportsInt | typing.SupportsIndex = 250, driftCorrectionBlurInterval: typing.SupportsInt | typing.SupportsIndex = 250) -> bool:
        ...
class DynamicsInitialization:
    @property
    def axisWeights(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]]:
        ...
    @axisWeights.setter
    def axisWeights(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]]) -> None:
        ...
    @property
    def bodyCom(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, n]"]:
        ...
    @bodyCom.setter
    def bodyCom(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, n]"]) -> None:
        ...
    @property
    def bodyInertia(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[6, n]"]:
        ...
    @bodyInertia.setter
    def bodyInertia(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[6, n]"]) -> None:
        ...
    @property
    def bodyMasses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @bodyMasses.setter
    def bodyMasses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def contactBodies(self) -> list[list[_nimblephysics.dynamics.BodyNode]]:
        ...
    @contactBodies.setter
    def contactBodies(self, arg0: collections.abc.Sequence[collections.abc.Sequence[_nimblephysics.dynamics.BodyNode]]) -> None:
        ...
    @property
    def defaultForcePlateCorners(self) -> list[list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @defaultForcePlateCorners.setter
    def defaultForcePlateCorners(self, arg0: collections.abc.Sequence[collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def forcePlateTrials(self) -> list[list[ForcePlate]]:
        ...
    @forcePlateTrials.setter
    def forcePlateTrials(self, arg0: collections.abc.Sequence[collections.abc.Sequence[ForcePlate]]) -> None:
        ...
    @property
    def grfBodyContactSphereRadius(self) -> list[list[list[float]]]:
        ...
    @grfBodyContactSphereRadius.setter
    def grfBodyContactSphereRadius(self, arg0: collections.abc.Sequence[collections.abc.Sequence[collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]]]) -> None:
        ...
    @property
    def grfBodyForceActive(self) -> list[list[list[bool]]]:
        ...
    @grfBodyForceActive.setter
    def grfBodyForceActive(self, arg0: collections.abc.Sequence[collections.abc.Sequence[collections.abc.Sequence[bool]]]) -> None:
        ...
    @property
    def grfBodyIndices(self) -> list[int]:
        ...
    @grfBodyIndices.setter
    def grfBodyIndices(self, arg0: collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex]) -> None:
        ...
    @property
    def grfBodyNodes(self) -> list[_nimblephysics.dynamics.BodyNode]:
        ...
    @grfBodyNodes.setter
    def grfBodyNodes(self, arg0: collections.abc.Sequence[_nimblephysics.dynamics.BodyNode]) -> None:
        ...
    @property
    def grfBodyOffForcePlate(self) -> list[list[list[bool]]]:
        ...
    @grfBodyOffForcePlate.setter
    def grfBodyOffForcePlate(self, arg0: collections.abc.Sequence[collections.abc.Sequence[collections.abc.Sequence[bool]]]) -> None:
        ...
    @property
    def grfBodySphereInContact(self) -> list[list[list[bool]]]:
        ...
    @grfBodySphereInContact.setter
    def grfBodySphereInContact(self, arg0: collections.abc.Sequence[collections.abc.Sequence[collections.abc.Sequence[bool]]]) -> None:
        ...
    @property
    def grfTrials(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]]:
        ...
    @grfTrials.setter
    def grfTrials(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> None:
        ...
    @property
    def groupMasses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @groupMasses.setter
    def groupMasses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def groupScales(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @groupScales.setter
    def groupScales(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def includeTrialsInDynamicsFit(self) -> list[bool]:
        ...
    @includeTrialsInDynamicsFit.setter
    def includeTrialsInDynamicsFit(self, arg0: collections.abc.Sequence[bool]) -> None:
        ...
    @property
    def initialGroupCOMs(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @initialGroupCOMs.setter
    def initialGroupCOMs(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def initialGroupInertias(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @initialGroupInertias.setter
    def initialGroupInertias(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def initialGroupMasses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @initialGroupMasses.setter
    def initialGroupMasses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def initialGroupScales(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @initialGroupScales.setter
    def initialGroupScales(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def initialMarkerOffsets(self) -> dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @initialMarkerOffsets.setter
    def initialMarkerOffsets(self, arg0: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def jointAxis(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]]:
        ...
    @jointAxis.setter
    def jointAxis(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> None:
        ...
    @property
    def jointCenters(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]]:
        ...
    @jointCenters.setter
    def jointCenters(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> None:
        ...
    @property
    def jointWeights(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]]:
        ...
    @jointWeights.setter
    def jointWeights(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]]) -> None:
        ...
    @property
    def joints(self) -> list[list[_nimblephysics.dynamics.Joint]]:
        ...
    @joints.setter
    def joints(self, arg0: collections.abc.Sequence[collections.abc.Sequence[_nimblephysics.dynamics.Joint]]) -> None:
        ...
    @property
    def jointsAdjacentMarkers(self) -> list[list[list[str]]]:
        ...
    @jointsAdjacentMarkers.setter
    def jointsAdjacentMarkers(self, arg0: collections.abc.Sequence[collections.abc.Sequence[collections.abc.Sequence[str]]]) -> None:
        ...
    @property
    def markerObservationTrials(self) -> list[list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]]:
        ...
    @markerObservationTrials.setter
    def markerObservationTrials(self, arg0: collections.abc.Sequence[collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]]) -> None:
        ...
    @property
    def markerOffsets(self) -> dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @markerOffsets.setter
    def markerOffsets(self, arg0: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def missingGRFReason(self) -> list[list[MissingGRFReason]]:
        ...
    @missingGRFReason.setter
    def missingGRFReason(self, arg0: collections.abc.Sequence[collections.abc.Sequence[MissingGRFReason]]) -> None:
        ...
    @property
    def originalPoses(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]]:
        ...
    @originalPoses.setter
    def originalPoses(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> None:
        ...
    @property
    def poseTrials(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]]:
        ...
    @poseTrials.setter
    def poseTrials(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> None:
        ...
    @property
    def probablyMissingGRF(self) -> list[list[MissingGRFStatus]]:
        ...
    @probablyMissingGRF.setter
    def probablyMissingGRF(self, arg0: collections.abc.Sequence[collections.abc.Sequence[MissingGRFStatus]]) -> None:
        ...
    @property
    def regularizeGroupCOMsTo(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @regularizeGroupCOMsTo.setter
    def regularizeGroupCOMsTo(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def regularizeGroupInertiasTo(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @regularizeGroupInertiasTo.setter
    def regularizeGroupInertiasTo(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def regularizeGroupMassesTo(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @regularizeGroupMassesTo.setter
    def regularizeGroupMassesTo(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def regularizeGroupScalesTo(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @regularizeGroupScalesTo.setter
    def regularizeGroupScalesTo(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def regularizeMarkerOffsetsTo(self) -> dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @regularizeMarkerOffsetsTo.setter
    def regularizeMarkerOffsetsTo(self, arg0: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def trackingMarkers(self) -> list[str]:
        ...
    @trackingMarkers.setter
    def trackingMarkers(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
    @property
    def trialTimesteps(self) -> list[float]:
        ...
    @trialTimesteps.setter
    def trialTimesteps(self, arg0: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
    @property
    def trialsOnTreadmill(self) -> list[bool]:
        ...
    @trialsOnTreadmill.setter
    def trialsOnTreadmill(self, arg0: collections.abc.Sequence[bool]) -> None:
        ...
    @property
    def updatedMarkerMap(self) -> dict[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @updatedMarkerMap.setter
    def updatedMarkerMap(self, arg0: collections.abc.Mapping[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
class ForcePlate:
    @staticmethod
    def copyForcePlate(plate: ForcePlate) -> ForcePlate:
        ...
    def __init__(self) -> None:
        ...
    def autodetectNoiseThresholdAndClip(self, percentOfMaxToDetectThumb: typing.SupportsFloat | typing.SupportsIndex = 0.25, percentOfMaxToCheckThumbRightEdge: typing.SupportsFloat | typing.SupportsIndex = 0.35) -> None:
        ...
    def detectAndFixCopMomentConvention(self, trial: typing.SupportsInt | typing.SupportsIndex = -1, i: typing.SupportsInt | typing.SupportsIndex = -1) -> None:
        ...
    def getResamplingMatrixAndGroundHeights(self) -> tuple[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"], typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]]:
        ...
    def setResamplingMatrixAndGroundHeights(self, matrix: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], groundHeights: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    def trim(self, newStartTime: typing.SupportsFloat | typing.SupportsIndex, newEndTime: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def trimToIndexes(self, start: typing.SupportsInt | typing.SupportsIndex, end: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def centersOfPressure(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @centersOfPressure.setter
    def centersOfPressure(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def corners(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @corners.setter
    def corners(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def forces(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @forces.setter
    def forces(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def moments(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @moments.setter
    def moments(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def timestamps(self) -> list[float]:
        ...
    @timestamps.setter
    def timestamps(self, arg0: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
    @property
    def worldOrigin(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        ...
    @worldOrigin.setter
    def worldOrigin(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> None:
        ...
class Frame:
    """
    
            This is for doing ML and large-scale data analysis. This is a single frame of data, returned in a list by :code:`SubjectOnDisk.readFrames()`, which contains everything needed to reconstruct all the dynamics of a snapshot in time.
          
    """
    @property
    def accObservations(self) -> list[tuple[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        """
        This is list of :code:`Pair[str, np.ndarray]` of the accelerometers observations at this frame. Accelerometers that were not observed (perhaps due to time offsets in uploaded data) will not be present in this list. For the full specification of the accelerometer set, load the model from the :code:`SubjectOnDisk`
        """
    @accObservations.setter
    def accObservations(self, arg0: collections.abc.Sequence[tuple[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def customValues(self) -> list[tuple[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]]]:
        """
        This is list of :code:`Pair[str, np.ndarray]` of unspecified values. The idea here is to allow the format to be easily extensible with unusual data (for example, exoskeleton torques) without bloating ordinary training files.
        """
    @customValues.setter
    def customValues(self, arg0: collections.abc.Sequence[tuple[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]]]) -> None:
        ...
    @property
    def emgSignals(self) -> list[tuple[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]]]:
        """
        This is list of :code:`Pair[str, np.ndarray]` of the EMG signals at this frame. EMG signals are generally preserved at a higher sampling frequency than the motion capture, so the `np.ndarray` vector will be a number of samples that were captured during this single motion capture frame. For example, if EMG is at 1000Hz and mocap is at 100Hz, the `np.ndarray` vector will be of length 10.
        """
    @emgSignals.setter
    def emgSignals(self, arg0: collections.abc.Sequence[tuple[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]]]) -> None:
        ...
    @property
    def exoTorques(self) -> list[tuple[int, float]]:
        """
        This is list of :code:`Pair[int, np.ndarray]` of the DOF indices that are actuated by exoskeletons, and the torques on those DOFs.
        """
    @exoTorques.setter
    def exoTorques(self, arg0: collections.abc.Sequence[tuple[typing.SupportsInt | typing.SupportsIndex, typing.SupportsFloat | typing.SupportsIndex]]) -> None:
        ...
    @property
    def gyroObservations(self) -> list[tuple[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        """
        This is list of :code:`Pair[str, np.ndarray]` of the gyroscope observations at this frame. Gyroscopes that were not observed (perhaps due to time offsets in uploaded data) will not be present in this list. For the full specification of the gyroscope set, load the model from the :code:`SubjectOnDisk`
        """
    @gyroObservations.setter
    def gyroObservations(self, arg0: collections.abc.Sequence[tuple[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def markerObservations(self) -> list[tuple[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        """
        This is list of :code:`Pair[str, np.ndarray]` of the marker observations at this frame. Markers that were not observed will not be present in this list. For the full specification of the markerset, load the model from the :code:`SubjectOnDisk`
        """
    @markerObservations.setter
    def markerObservations(self, arg0: collections.abc.Sequence[tuple[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def missingGRFReason(self) -> MissingGRFReason:
        """
                    This is the reason that this frame is missing GRF, or else is the flag notMissingGRF to indicate that this frame has physics.
        
                    WARNING: If this is true, you can't trust the :code:`tau` or :code:`acc` values on this frame!!
        """
    @missingGRFReason.setter
    def missingGRFReason(self, arg0: MissingGRFReason) -> None:
        ...
    @property
    def processingPasses(self) -> FramePassList:
        """
                    The processing passes that were done on this Frame. For example, if we solved for kinematics, then dynamics, 
                    then low pass filtered, this will have 3 entries.
        """
    @processingPasses.setter
    def processingPasses(self, arg0: FramePassList) -> None:
        ...
    @property
    def rawForcePlateCenterOfPressures(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        """
        This is list of :code:`np.ndarray` of the original center of pressure readings on each force plate, without any processing by AddBiomechanics. These are the original inputs that were used to create this SubjectOnDisk.
        """
    @rawForcePlateCenterOfPressures.setter
    def rawForcePlateCenterOfPressures(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def rawForcePlateForces(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        """
        This is list of :code:`np.ndarray` of the original force readings on each force plate, without any processing by AddBiomechanics. These are the original inputs that were used to create this SubjectOnDisk.
        """
    @rawForcePlateForces.setter
    def rawForcePlateForces(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def rawForcePlateTorques(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        """
        This is list of :code:`np.ndarray` of the original torque readings on each force plate, without any processing by AddBiomechanics. These are the original inputs that were used to create this SubjectOnDisk.
        """
    @rawForcePlateTorques.setter
    def rawForcePlateTorques(self, arg0: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def t(self) -> int:
        """
        The frame number in this trial.
        """
    @t.setter
    def t(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def trial(self) -> int:
        """
        The index of the trial in the containing SubjectOnDisk.
        """
    @trial.setter
    def trial(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
class FrameList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Frame) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: FrameList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> FrameList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> Frame:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: FrameList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None:
        ...
    def __iter__(self) -> collections.abc.Iterator[Frame]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: FrameList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex, arg1: Frame) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FrameList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Frame) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Frame) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: FrameList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: typing.SupportsInt | typing.SupportsIndex, x: Frame) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Frame:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: typing.SupportsInt | typing.SupportsIndex) -> Frame:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Frame) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class FramePass:
    """
    
            This is for doing ML and large-scale data analysis. This is a single processing pass on a single frame of data, returned from a list within a :code:`nimblephysics.biomechanics.Frame` (which can be got with :code:`SubjectOnDisk.readFrames()`), which contains the full reconstruction of your subject at this instant created by this processing pass. Earlier processing passes are likely to have more discrepancies with the original data, bet later processing passes require more types of sensor signals that may not always be available.
          
    """
    @property
    def acc(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
        The joint accelerations on this frame.
        """
    @property
    def accFiniteDifferenced(self) -> typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]:
        """
        A boolean mask of [0,1]s for each DOF, with a 1 indicating that this DOF got its acceleration through finite differencing, and therefore may be somewhat unreliable
        """
    @property
    def angularResidual(self) -> float:
        """
        A scalar giving how much angular torque, in Newton-meters, would need to be applied at the root of the skeleton in order to enable the skeleton's observed accelerations (given positions and velocities) on this frame.
        """
    @property
    def comAcc(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        The acceleration of the COM, in world space
        """
    @property
    def comAccInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        This is the acceleration of the center of mass of the subject, expressed in the root body frame (which probably means expressed in pelvis coordinates, though some skeletons may use a different body as the root, for instance the torso).
        """
    @property
    def comPos(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        The position of the COM, in world space
        """
    @property
    def comVel(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        The velocity of the COM, in world space
        """
    @property
    def contact(self) -> typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]:
        """
        A vector of [0,1] booleans for if a body is in contact with the ground.
        """
    @property
    def groundContactCenterOfPressure(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
                    This is a vector of all the concatenated :code:`CoP` values for each contact body, where :code:`CoP` is a 3 vector representing the center of pressure for a contact measured on the force plate. :code:`CoP` is 
                    expressed in the world frame.
        """
    @property
    def groundContactCenterOfPressureInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
                    This is a vector of all the concatenated :code:`CoP` values for each contact body, where :code:`CoP` is a 3 vector representing the center of pressure for a contact measured on the force plate. :code:`CoP` is 
                    expressed in the root frame, which is a frame that is rigidly attached to the root body of the skeleton (probably the pelvis).
        """
    @property
    def groundContactForce(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
                    This is a vector of all the concatenated :code:`f` values for each contact body, where :code:`f` is a 3 vector representing the ground-reaction force from a contact, measured on the force plate. :code:`f` is 
                    expressed in the world frame, and is assumed to be acting at the corresponding :code:`CoP` from the same index in :code:`groundContactCenterOfPressure`.
        """
    @property
    def groundContactForceInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
                    This is a vector of all the concatenated :code:`f` values for each contact body, where :code:`f` is a 3 vector representing the ground-reaction force from a contact, measured on the force plate. :code:`f` is 
                    expressed in the root frame, which is a frame that is rigidly attached to the root body of the skeleton (probably the pelvis), and is assumed to be acting at the corresponding :code:`CoP` from the same index in :code:`groundContactCenterOfPressure`.
        """
    @property
    def groundContactTorque(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
                    This is a vector of all the concatenated :code:`tau` values for each contact body, where :code:`tau` is a 3 vector representing the ground-reaction torque from a contact, measured on the force plate. :code:`tau` is 
                    expressed in the world frame, and is assumed to be acting at the corresponding :code:`CoP` from the same index in :code:`groundContactCenterOfPressure`.
        """
    @property
    def groundContactTorqueInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
                    This is a vector of all the concatenated :code:`tau` values for each contact body, where :code:`tau` is a 3 vector representing the ground-reaction torque from a contact, measured on the force plate. :code:`tau` is 
                    expressed in the root frame, which is a frame that is rigidly attached to the root body of the skeleton (probably the pelvis), and is assumed to be acting at the corresponding :code:`CoP` from the same index in :code:`groundContactCenterOfPressure`.
        """
    @property
    def groundContactWrenches(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
        This is a vector of concatenated contact body wrenches :code:`body_wrench`, where :code:`body_wrench` is a 6 vector (first 3 are torque, last 3 are force). 
        :code:`body_wrench` is expressed in the local frame of the body at :code:`body_name`, and assumes that the skeleton is set to positions `pos`.
        
        Here's an example usage
        .. code-block::
            for i, bodyName in enumerate(subject.getContactBodies()):
                body: nimble.dynamics.BodyNode = skel.getBodyNode(bodyName)
                torque_local = wrench[i*6:i*6+3]
                force_local = wrench[i*6+3:i*6+6]
                # For example, to rotate the force to the world frame
                R_wb = body.getWorldTransform().rotation()
                force_world = R_wb @ force_local
        
        Note that these are specified in the local body frame, acting on the body at its origin, so transforming them to the world frame requires a transformation!
        """
    @property
    def groundContactWrenchesInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
        These are the wrenches (each vectors of length 6, composed of first 3 = torque, last 3 = force) expressed in the root body frame, and concatenated together. The root body is probably the pelvis, but for some skeletons they may use another body as the root, like the torso.
        """
    @property
    def jointCenters(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
        These are the joint center locations, concatenated together, given in the world frame.
        """
    @property
    def jointCentersInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
        These are the joint center locations, concatenated together, given in the root frame. The root body is probably the pelvis, but for some skeletons they may use another body as the root, like the torso.
        """
    @property
    def linearResidual(self) -> float:
        """
        A scalar giving how much linear force, in Newtons, would need to be applied at the root of the skeleton in order to enable the skeleton's observed accelerations (given positions and velocities) on this frame.
        """
    @property
    def markerMax(self) -> float:
        """
        A scalar indicating the maximum marker error (discrepancy between the model and the experimentally observed marker locations) on this frame, in meters, with these joint positions.
        """
    @property
    def markerRMS(self) -> float:
        """
        A scalar indicating the RMS marker error (discrepancy between the model and the experimentally observed marker locations) on this frame, in meters, with these joint positions.
        """
    @property
    def pos(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
        The joint positions on this frame.
        """
    @property
    def posObserved(self) -> typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]:
        """
        A boolean mask of [0,1]s for each DOF, with a 1 indicating that this DOF was observed on this frame
        """
    @property
    def residualWrenchInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[6, 1]"]:
        """
        This is the 'residual' force wrench (or 'modelling error' force, the force necessary to make Newton's laws match up with our model, even though it's imaginary) expressed in the root body frame. This is a wrench (vector of length 6, composed of first 3 = torque, last 3 = force). The root body is probably the pelvis, but for some skeletons they may use another body as the root, like the torso.
        """
    @property
    def rootAngularAccInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        This is the angular velocity, in an angle-axis representation where the norm of this 3-vector is given in radians per second squared, of the root body of the skeleton (probably the pelvis) expressed in its own coordinate frame.
        """
    @property
    def rootAngularVelInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        This is the angular velocity, in an angle-axis representation where the norm of this 3-vector is given in radians per second, of the root body of the skeleton (probably the pelvis) expressed in its own coordinate frame.
        """
    @property
    def rootEulerHistoryInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
        This is the recent history of the angles (expressed as euler angles) of the root body of the skeleton (probably the pelvis) expressed in its own coordinate frame.
        """
    @property
    def rootLinearAccInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        This is the linear acceleration, in meters per second squared, of the root body of the skeleton (probably the pelvis) expressed in its own coordinate frame.
        """
    @property
    def rootLinearVelInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        This is the linear velocity, in meters per second, of the root body of the skeleton (probably the pelvis) expressed in its own coordinate frame.
        """
    @property
    def rootPosHistoryInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
        This is the recent history of the positions of the root body of the skeleton (probably the pelvis) expressed in its own coordinate frame. These are concatenated 3-vectors. The [0:3] of the vector is the most recent, and they get older from there. Vectors  
        """
    @property
    def tau(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
        The joint control forces on this frame.
        """
    @property
    def type(self) -> ProcessingPassType:
        """
        The type of processing pass that this data came from. Options include KINEMATICS (for movement only), DYNAMICS (for movement and physics), and LOW_PASS_FILTER (to apply a simple Butterworth to the observed data from the previous pass).
        """
    @property
    def vel(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        """
        The joint velocities on this frame.
        """
    @property
    def velFiniteDifferenced(self) -> typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]:
        """
        A boolean mask of [0,1]s for each DOF, with a 1 indicating that this DOF got its velocity through finite differencing, and therefore may be somewhat unreliable
        """
class FramePassList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: FramePass) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: FramePassList) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> FramePassList:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> FramePass:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: FramePassList) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None:
        ...
    def __iter__(self) -> collections.abc.Iterator[FramePass]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: FramePassList) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex, arg1: FramePass) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: FramePassList) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: FramePass) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: FramePass) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: FramePassList) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: typing.SupportsInt | typing.SupportsIndex, x: FramePass) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> FramePass:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: typing.SupportsInt | typing.SupportsIndex) -> FramePass:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: FramePass) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class IKErrorReport:
    def __init__(self, skeleton: _nimblephysics.dynamics.Skeleton, markers: collections.abc.Mapping[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], poses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], observations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    def getSortedMarkerRMSE(self) -> list[tuple[str, float]]:
        ...
    def printReport(self, limitTimesteps: typing.SupportsInt | typing.SupportsIndex = -1) -> None:
        ...
    def saveCSVMarkerErrorReport(self, path: str) -> None:
        ...
    @property
    def averageMaxError(self) -> float:
        ...
    @averageMaxError.setter
    def averageMaxError(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    @property
    def averageRootMeanSquaredError(self) -> float:
        ...
    @averageRootMeanSquaredError.setter
    def averageRootMeanSquaredError(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    @property
    def averageSumSquaredError(self) -> float:
        ...
    @averageSumSquaredError.setter
    def averageSumSquaredError(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    @property
    def maxError(self) -> list[float]:
        ...
    @maxError.setter
    def maxError(self, arg0: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
    @property
    def rootMeanSquaredError(self) -> list[float]:
        ...
    @rootMeanSquaredError.setter
    def rootMeanSquaredError(self, arg0: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
    @property
    def sumSquaredError(self) -> list[float]:
        ...
    @sumSquaredError.setter
    def sumSquaredError(self, arg0: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
class IMUFineTuneProblem:
    def flatten(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getAccs(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getGrad(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getLoss(self) -> float:
        ...
    def getPoses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getProblemSize(self) -> int:
        ...
    def getVels(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def setWeightAccs(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setWeightGyros(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setWeightPoses(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def unflatten(self, x: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
class InitialMarkerFitParams:
    dontRescaleBodies: bool
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def setApplyInnerProblemGradientConstraints(self, applyConstraints: bool) -> InitialMarkerFitParams:
        ...
    def setDontRescaleBodies(self, dontRescaleBodies: bool) -> InitialMarkerFitParams:
        ...
    def setGroupScales(self, groupScales: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> InitialMarkerFitParams:
        ...
    def setInitPoses(self, initPoses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> InitialMarkerFitParams:
        ...
    def setJointCenters(self, joints: collections.abc.Sequence[_nimblephysics.dynamics.Joint], jointCenters: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], jointAdjacentMarkers: collections.abc.Sequence[collections.abc.Sequence[str]]) -> InitialMarkerFitParams:
        ...
    def setJointCentersAndWeights(self, joints: collections.abc.Sequence[_nimblephysics.dynamics.Joint], jointCenters: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], jointAdjacentMarkers: collections.abc.Sequence[collections.abc.Sequence[str]], jointWeights: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> InitialMarkerFitParams:
        ...
    def setMarkerOffsets(self, markerOffsets: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> InitialMarkerFitParams:
        ...
    def setMarkerWeights(self, markerWeights: collections.abc.Mapping[str, typing.SupportsFloat | typing.SupportsIndex]) -> InitialMarkerFitParams:
        ...
    def setMaxTimestepsToUseForMultiTrialScaling(self, numTimesteps: typing.SupportsInt | typing.SupportsIndex) -> InitialMarkerFitParams:
        ...
    def setMaxTrialsToUseForMultiTrialScaling(self, numTrials: typing.SupportsInt | typing.SupportsIndex) -> InitialMarkerFitParams:
        ...
    def setNumBlocks(self, numBlocks: typing.SupportsInt | typing.SupportsIndex) -> InitialMarkerFitParams:
        ...
    def setNumIKTries(self, tries: typing.SupportsInt | typing.SupportsIndex) -> InitialMarkerFitParams:
        ...
    def setSkipBilevel(self, skipBilevel: bool) -> InitialMarkerFitParams:
        ...
    def setUseAnalyticalIKToInitialize(self, useAnalyticalIK: bool) -> InitialMarkerFitParams:
        ...
    @property
    def groupScales(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @groupScales.setter
    def groupScales(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def initPoses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @initPoses.setter
    def initPoses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def jointCenters(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @jointCenters.setter
    def jointCenters(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def jointWeights(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @jointWeights.setter
    def jointWeights(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def joints(self) -> list[_nimblephysics.dynamics.Joint]:
        ...
    @joints.setter
    def joints(self, arg0: collections.abc.Sequence[_nimblephysics.dynamics.Joint]) -> None:
        ...
    @property
    def markerOffsets(self) -> dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @markerOffsets.setter
    def markerOffsets(self, arg0: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def markerWeights(self) -> dict[str, float]:
        ...
    @markerWeights.setter
    def markerWeights(self, arg0: collections.abc.Mapping[str, typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
    @property
    def maxTimestepsToUseForMultiTrialScaling(self) -> int:
        ...
    @maxTimestepsToUseForMultiTrialScaling.setter
    def maxTimestepsToUseForMultiTrialScaling(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def maxTrialsToUseForMultiTrialScaling(self) -> int:
        ...
    @maxTrialsToUseForMultiTrialScaling.setter
    def maxTrialsToUseForMultiTrialScaling(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def numBlocks(self) -> int:
        ...
    @numBlocks.setter
    def numBlocks(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
class LabelledMarkers:
    @property
    def jointCenterGuesses(self) -> list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @jointCenterGuesses.setter
    def jointCenterGuesses(self, arg0: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def markerObservations(self) -> list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @markerObservations.setter
    def markerObservations(self, arg0: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def markerOffsets(self) -> dict[str, tuple[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @markerOffsets.setter
    def markerOffsets(self, arg0: collections.abc.Mapping[str, tuple[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def traces(self) -> list[MarkerTrace]:
        ...
    @traces.setter
    def traces(self, arg0: collections.abc.Sequence[MarkerTrace]) -> None:
        ...
class LilypadSolver:
    def __init__(self, skeleton: _nimblephysics.dynamics.Skeleton, groundContactBodies: collections.abc.Sequence[_nimblephysics.dynamics.BodyNode], groundNormal: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], tileSize: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def clear(self) -> None:
        ...
    def debugToGUI(self, gui: ...) -> None:
        ...
    def getContactBodies(self) -> list[_nimblephysics.dynamics.BodyNode]:
        ...
    def process(self, poses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], startTime: typing.SupportsInt | typing.SupportsIndex = 0) -> None:
        ...
    def setLateralVelThreshold(self, threshold: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setVerticalAccelerationThreshold(self, threshold: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setVerticalVelThreshold(self, threshold: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
class LinkBeam:
    def __init__(self, cost: typing.SupportsFloat | typing.SupportsIndex, a_label: str, a_observed_this_timestep: bool, a_last_observed_point: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], a_last_observed_timestamp: typing.SupportsFloat | typing.SupportsIndex, a_last_observed_velocity: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], b_label: str, b_observed_this_timestep: bool, b_last_observed_point: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], b_last_observed_timestamp: typing.SupportsFloat | typing.SupportsIndex, b_last_observed_velocity: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], parent: LinkBeam = None) -> None:
        ...
    @property
    def a_label(self) -> str:
        ...
    @property
    def a_last_observed_point(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @property
    def a_last_observed_timestamp(self) -> float:
        ...
    @property
    def a_last_observed_velocity(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @property
    def a_observed_this_timestep(self) -> bool:
        ...
    @property
    def b_label(self) -> str:
        ...
    @property
    def b_last_observed_point(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @property
    def b_last_observed_timestamp(self) -> float:
        ...
    @property
    def b_last_observed_velocity(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @property
    def b_observed_this_timestep(self) -> bool:
        ...
    @property
    def cost(self) -> float:
        ...
    @property
    def parent(self) -> ...:
        ...
class LinkBeamSearch:
    @staticmethod
    def convert_to_traces(beam: LinkBeam) -> tuple[list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]], list[float], str, list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]], list[float], str]:
        ...
    @staticmethod
    def process_markers(label_pairs: collections.abc.Sequence[tuple[str, str]], marker_observations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]]], timestamps: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex], beam_width: typing.SupportsInt | typing.SupportsIndex = 5, pair_weight: typing.SupportsFloat | typing.SupportsIndex = 100.0, pair_threshold: typing.SupportsFloat | typing.SupportsIndex = 0.01, vel_weight: typing.SupportsFloat | typing.SupportsIndex = 0.1, vel_threshold: typing.SupportsFloat | typing.SupportsIndex = 5.0, acc_weight: typing.SupportsFloat | typing.SupportsIndex = 0.001, acc_threshold: typing.SupportsFloat | typing.SupportsIndex = 1000.0, print_updates: bool = True, multithread: bool = True) -> tuple[list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]]], list[float]]:
        ...
    @staticmethod
    def search(a_label: str, b_label: str, marker_observations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]]], timestamps: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex], beam_width: typing.SupportsInt | typing.SupportsIndex = 5, pair_weight: typing.SupportsFloat | typing.SupportsIndex = 100.0, pair_threshold: typing.SupportsFloat | typing.SupportsIndex = 0.01, vel_weight: typing.SupportsFloat | typing.SupportsIndex = 1.0, vel_threshold: typing.SupportsFloat | typing.SupportsIndex = 5.0, acc_weight: typing.SupportsFloat | typing.SupportsIndex = 0.001, acc_threshold: typing.SupportsFloat | typing.SupportsIndex = 1000.0, print_updates: bool = True) -> tuple[list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]], list[float], str, list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]], list[float], str]:
        ...
    def __init__(self, seed_a_point: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], seed_a_label: str, seed_b_point: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], seed_b_label: str, seed_timestamp: typing.SupportsFloat | typing.SupportsIndex, pair_dist: typing.SupportsFloat | typing.SupportsIndex, pair_weight: typing.SupportsFloat | typing.SupportsIndex = 100.0, pair_threshold: typing.SupportsFloat | typing.SupportsIndex = 0.01, vel_weight: typing.SupportsFloat | typing.SupportsIndex = 1.0, vel_threshold: typing.SupportsFloat | typing.SupportsIndex = 5.0, acc_weight: typing.SupportsFloat | typing.SupportsIndex = 0.001, acc_threshold: typing.SupportsFloat | typing.SupportsIndex = 1000.0) -> None:
        ...
    def make_next_generation(self, markers: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], timestamp: typing.SupportsFloat | typing.SupportsIndex, beam_width: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def prune_beams(self, beam_width: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def beams(self) -> list[LinkBeam]:
        ...
class MarkerBeamSearch:
    @staticmethod
    def convert_to_trace(beam: Beam) -> tuple[list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]], list[float], str]:
        ...
    @staticmethod
    def search(label: str, marker_observations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], timestamps: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex], beam_width: typing.SupportsInt | typing.SupportsIndex = 20, vel_threshold: typing.SupportsFloat | typing.SupportsIndex = 7.0, acc_threshold: typing.SupportsFloat | typing.SupportsIndex = 2000.0) -> tuple[list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]], list[float], str]:
        ...
    def __init__(self, seed_point: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], seed_timestamp: typing.SupportsFloat | typing.SupportsIndex, seed_label: str, vel_threshold: typing.SupportsFloat | typing.SupportsIndex = 7.0, acc_threshold: typing.SupportsFloat | typing.SupportsIndex = 2000.0) -> None:
        ...
    def make_next_generation(self, markers: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]], timestamp: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def prune_beams(self, beam_width: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def beams(self) -> list[Beam]:
        ...
class MarkerFitter:
    @staticmethod
    def getMarkerLossGradientWrtJoints(skeleton: _nimblephysics.dynamics.Skeleton, markers: collections.abc.Sequence[tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], lossGradWrtMarkerError: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @staticmethod
    def pickSubset(markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], subsetSize: typing.SupportsInt | typing.SupportsIndex) -> list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    def __init__(self, skeleton: _nimblephysics.dynamics.Skeleton, markers: collections.abc.Mapping[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], ignoreVirtualJointCenterMarkers: bool = False) -> None:
        ...
    def addZeroConstraint(self, name: str, loss: collections.abc.Callable[[MarkerFitterState], float]) -> None:
        ...
    def autorotateC3D(self, c3d: C3D) -> None:
        ...
    def checkForEnoughMarkers(self, markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> bool:
        ...
    def checkForFlippedMarkers(self, markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], init: MarkerInitialization, report: MarkersErrorReport) -> bool:
        ...
    def debugTrajectoryAndMarkersToGUI(self, server: ..., init: MarkerInitialization, markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], forcePlates: collections.abc.Sequence[ForcePlate] = None, goldOsim: OpenSimFile = None, goldPoses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"] = ...) -> None:
        ...
    def findJointCenters(self, initializations: MarkerInitialization, newClip: collections.abc.Sequence[bool], markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    def fineTuneWithIMU(self, accObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], gyroObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], newClip: collections.abc.Sequence[bool], init: MarkerInitialization, dt: typing.SupportsFloat | typing.SupportsIndex, weightAccs: typing.SupportsFloat | typing.SupportsIndex = 1.0, weightGyros: typing.SupportsFloat | typing.SupportsIndex = 1.0, weightMarkers: typing.SupportsFloat | typing.SupportsIndex = 100.0, regularizePoses: typing.SupportsFloat | typing.SupportsIndex = 1.0, useIPOPT: bool = True, iterations: typing.SupportsInt | typing.SupportsIndex = 300, lbfgsMemory: typing.SupportsInt | typing.SupportsIndex = 100) -> MarkerInitialization:
        ...
    def generateDataErrorsReport(self, markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], dt: typing.SupportsFloat | typing.SupportsIndex, rippleReduce: bool = True, rippleReduceUseSparse: bool = True, rippleReduceUseIterativeSolver: bool = True, rippleReduceSolverIterations: typing.SupportsInt | typing.SupportsIndex = 100000.0) -> MarkersErrorReport:
        ...
    def getIMUFineTuneProblem(self, accObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], gyroObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], init: MarkerInitialization, dt: typing.SupportsFloat | typing.SupportsIndex, start: typing.SupportsInt | typing.SupportsIndex, end: typing.SupportsInt | typing.SupportsIndex) -> IMUFineTuneProblem:
        ...
    def getImuList(self) -> list[tuple[_nimblephysics.dynamics.BodyNode, _nimblephysics.math.Isometry3]]:
        ...
    def getImuMap(self) -> dict[str, tuple[_nimblephysics.dynamics.BodyNode, _nimblephysics.math.Isometry3]]:
        ...
    def getImuNames(self) -> list[str]:
        ...
    def getInitialization(self, markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], newClip: collections.abc.Sequence[bool], params: InitialMarkerFitParams = ...) -> MarkerInitialization:
        ...
    def getMarkerIsTracking(self, marker: str) -> bool:
        ...
    def getNumMarkers(self) -> int:
        ...
    def measureAccelerometerRMS(self, accObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], newClip: collections.abc.Sequence[bool], init: MarkerInitialization, dt: typing.SupportsFloat | typing.SupportsIndex) -> float:
        ...
    def measureGyroRMS(self, gyroObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], newClip: collections.abc.Sequence[bool], init: MarkerInitialization, dt: typing.SupportsFloat | typing.SupportsIndex) -> float:
        ...
    def optimizeBilevel(self, markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], newClip: collections.abc.Sequence[bool], initialization: MarkerInitialization, numSamples: typing.SupportsInt | typing.SupportsIndex, applyInnerProblemGradientConstraints: bool = True) -> BilevelFitResult:
        ...
    def removeZeroConstraint(self, name: str) -> None:
        ...
    def rotateIMUs(self, accObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], gyroObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], newClip: collections.abc.Sequence[bool], init: MarkerInitialization, dt: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def runKinematicsPipeline(self, markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], newClip: collections.abc.Sequence[bool], params: InitialMarkerFitParams, numSamples: typing.SupportsInt | typing.SupportsIndex = 20, skipFinalIK: bool = False) -> MarkerInitialization:
        ...
    def runMultiTrialKinematicsPipeline(self, markerTrials: collections.abc.Sequence[collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]], params: InitialMarkerFitParams, numSamples: typing.SupportsInt | typing.SupportsIndex = 50) -> list[MarkerInitialization]:
        ...
    def runPrescaledPipeline(self, markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], params: InitialMarkerFitParams) -> MarkerInitialization:
        ...
    def saveTrajectoryAndMarkersToGUI(self, path: str, init: MarkerInitialization, markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], accObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], gyroObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], frameRate: typing.SupportsInt | typing.SupportsIndex, forcePlates: collections.abc.Sequence[ForcePlate] = None, goldOsim: OpenSimFile = None, goldPoses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"] = ...) -> None:
        ...
    def setAnatomicalMarkerDefaultWeight(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setAnthropometricPrior(self, prior: Anthropometrics, weight: typing.SupportsFloat | typing.SupportsIndex = 0.001) -> None:
        ...
    def setCustomLossAndGrad(self, loss: collections.abc.Callable[[MarkerFitterState], float]) -> None:
        ...
    def setDebugJointVariability(self, debug: bool) -> None:
        ...
    def setDebugLoss(self, debug: bool) -> None:
        ...
    def setExplicitHeightPrior(self, prior: typing.SupportsFloat | typing.SupportsIndex, weight: typing.SupportsFloat | typing.SupportsIndex = 1000.0) -> None:
        ...
    def setIgnoreJointLimits(self, ignore: bool) -> None:
        ...
    def setImuMap(self, imuMap: collections.abc.Mapping[str, tuple[_nimblephysics.dynamics.BodyNode, _nimblephysics.math.Isometry3]]) -> None:
        ...
    def setInitialIKMaxRestarts(self, starts: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setInitialIKSatisfactoryLoss(self, loss: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setIterationLimit(self, iters: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setJointAxisFitSGDIterations(self, iters: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setJointForceFieldSoftness(self, softness: typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
          Larger values will increase the softness of the threshold penalty. Smaller
          values, as they approach zero, will have an almost perfectly vertical
          penality for going below the threshold distance. That would be hard to
          optimize, so don't make it too small.
        """
    def setJointForceFieldThresholdDistance(self, minDistance: typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
          This sets the minimum distance joints have to be apart in order to get
          zero "force field" loss. Any joints closer than this (in world space) will
          incur a penalty.
        """
    def setJointSphereFitSGDIterations(self, iters: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setLBFGSHistory(self, historyLen: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setMarkerIsTracking(self, marker: str, isTracking: bool = True) -> None:
        ...
    def setMaxAxisWeight(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setMaxJointWeight(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setMaxMarkerOffset(self, offset: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setMinAxisFitScore(self, score: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setMinJointVarianceCutoff(self, cutoff: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setMinSphereFitScore(self, score: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setParallelIKWarps(self, parallelWarps: bool) -> None:
        """
        If True, this processes "single threaded" IK tasks 32 timesteps at a time
                    (a "warp"), in parallel, using the first timestep of the warp as the
                    initialization for the whole warp. Defaults to False.
        """
    def setPostprocessAnatomicalMarkerOffsets(self, postprocess: bool) -> None:
        """
          If we set this to true, then after the main optimization completes we will
          do a final step to "center" the error of the anatomical markers. This
          minimizes marker RMSE, but does NOT respect the weights about how far
          markers should be allowed to move.
        """
    def setPostprocessTrackingMarkerOffsets(self, postprocess: bool) -> None:
        """
          If we set this to true, then after the main optimization completes we will
          do a final step to "center" the error of the tracking markers. This
          minimizes marker RMSE, but does NOT respect the weights about how far
          markers should be allowed to move.
        """
    def setRegularizeAllBodyScales(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setRegularizeAnatomicalMarkerOffsets(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setRegularizeIndividualBodyScales(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setRegularizeJointBounds(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setRegularizeJointWithVirtualSpring(self, jointName: str, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setRegularizeMovementSmoothness(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setRegularizePelvisJointsWithVirtualSpring(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setRegularizeTrackingMarkerOffsets(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setStaticTrial(self, markerObservationsMapAtStaticPose: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]], staticPose: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    def setStaticTrialWeight(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setTrackingMarkerDefaultWeight(self, weight: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setTrackingMarkers(self, trackingMarkerNames: collections.abc.Sequence[str]) -> None:
        ...
    def setTriadsToTracking(self) -> None:
        ...
    def writeCSVData(self, path: str, init: MarkerInitialization, rmsMarkerErrors: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex], maxMarkerErrors: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex], timestamps: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
class MarkerFitterState:
    @property
    def bodyNames(self) -> list[str]:
        ...
    @bodyNames.setter
    def bodyNames(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
    @property
    def bodyScales(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, n]"]:
        ...
    @bodyScales.setter
    def bodyScales(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, n]"]) -> None:
        ...
    @property
    def bodyScalesGrad(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, n]"]:
        ...
    @bodyScalesGrad.setter
    def bodyScalesGrad(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, n]"]) -> None:
        ...
    @property
    def jointErrorsAtTimesteps(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @jointErrorsAtTimesteps.setter
    def jointErrorsAtTimesteps(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def jointErrorsAtTimestepsGrad(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @jointErrorsAtTimestepsGrad.setter
    def jointErrorsAtTimestepsGrad(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def jointOrder(self) -> list[str]:
        ...
    @jointOrder.setter
    def jointOrder(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
    @property
    def markerErrorsAtTimesteps(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @markerErrorsAtTimesteps.setter
    def markerErrorsAtTimesteps(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def markerErrorsAtTimestepsGrad(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @markerErrorsAtTimestepsGrad.setter
    def markerErrorsAtTimestepsGrad(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def markerOffsets(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, n]"]:
        ...
    @markerOffsets.setter
    def markerOffsets(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, n]"]) -> None:
        ...
    @property
    def markerOffsetsGrad(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, n]"]:
        ...
    @markerOffsetsGrad.setter
    def markerOffsetsGrad(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, n]"]) -> None:
        ...
    @property
    def markerOrder(self) -> list[str]:
        ...
    @markerOrder.setter
    def markerOrder(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
    @property
    def posesAtTimesteps(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @posesAtTimesteps.setter
    def posesAtTimesteps(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def posesAtTimestepsGrad(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @posesAtTimestepsGrad.setter
    def posesAtTimestepsGrad(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
class MarkerFixer:
    @staticmethod
    def generateDataErrorsReport(immutableMarkerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], dt: typing.SupportsFloat | typing.SupportsIndex, dropProlongedStillness: bool = False, rippleReduce: bool = True, rippleReduceUseSparse: bool = True, rippleReduceUseIterativeSolver: bool = True, rippleReduceSolverIterations: typing.SupportsInt | typing.SupportsIndex = 100000.0) -> MarkersErrorReport:
        ...
class MarkerInitialization:
    error: bool
    errorMsg: str
    def __init__(self) -> None:
        ...
    @property
    def axisWeights(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @axisWeights.setter
    def axisWeights(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def groupScales(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @groupScales.setter
    def groupScales(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def jointAxis(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @jointAxis.setter
    def jointAxis(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def jointCenters(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @jointCenters.setter
    def jointCenters(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def jointWeights(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @jointWeights.setter
    def jointWeights(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def joints(self) -> list[_nimblephysics.dynamics.Joint]:
        ...
    @joints.setter
    def joints(self, arg0: collections.abc.Sequence[_nimblephysics.dynamics.Joint]) -> None:
        ...
    @property
    def jointsAdjacentMarkers(self) -> list[list[str]]:
        ...
    @jointsAdjacentMarkers.setter
    def jointsAdjacentMarkers(self, arg0: collections.abc.Sequence[collections.abc.Sequence[str]]) -> None:
        ...
    @property
    def markerOffsets(self) -> dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @markerOffsets.setter
    def markerOffsets(self, arg0: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def poses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @poses.setter
    def poses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def updatedMarkerMap(self) -> dict[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @updatedMarkerMap.setter
    def updatedMarkerMap(self, arg0: collections.abc.Mapping[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
class MarkerLabeller:
    def evaluate(self, markerOffsets: collections.abc.Mapping[str, tuple[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], labeledPointClouds: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    def guessJointLocations(self, pointClouds: collections.abc.Sequence[collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    def labelPointClouds(self, pointClouds: collections.abc.Sequence[collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], mergeMarkersThreshold: typing.SupportsFloat | typing.SupportsIndex = 0.01) -> LabelledMarkers:
        ...
    def matchUpJointToSkeletonJoint(self, jointName: str, skeletonJointName: str) -> None:
        ...
    def setSkeleton(self, skeleton: _nimblephysics.dynamics.Skeleton) -> None:
        ...
class MarkerLabellerMock(MarkerLabeller):
    def __init__(self) -> None:
        ...
    def setMockJointLocations(self, jointsOverTime: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
class MarkerMultiBeamSearch:
    @staticmethod
    def convert_to_traces(beam: MultiBeam) -> tuple[list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]], list[float]]:
        ...
    @staticmethod
    def get_median_70_percent_mean_distance(arg0: str, arg1: str, arg2: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> float:
        ...
    @staticmethod
    def process_markers(label_groups: collections.abc.Sequence[collections.abc.Sequence[str]], marker_observations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], timestamps: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex], beam_width: typing.SupportsInt | typing.SupportsIndex = 20, pair_weight: typing.SupportsFloat | typing.SupportsIndex = 100.0, pair_threshold: typing.SupportsFloat | typing.SupportsIndex = 0.001, vel_weight: typing.SupportsFloat | typing.SupportsIndex = 0.1, vel_threshold: typing.SupportsFloat | typing.SupportsIndex = 5.0, acc_weight: typing.SupportsFloat | typing.SupportsIndex = 0.001, acc_threshold: typing.SupportsFloat | typing.SupportsIndex = 500.0, print_interval: typing.SupportsInt | typing.SupportsIndex = 1000, crysatilize_interval: typing.SupportsInt | typing.SupportsIndex = 1000, multithread: bool = True) -> tuple[list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]], list[float]]:
        ...
    @staticmethod
    def search(labels: collections.abc.Sequence[str], marker_observations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], timestamps: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex], beam_width: typing.SupportsInt | typing.SupportsIndex = 20, pair_weight: typing.SupportsFloat | typing.SupportsIndex = 100.0, pair_threshold: typing.SupportsFloat | typing.SupportsIndex = 0.01, vel_weight: typing.SupportsFloat | typing.SupportsIndex = 1.0, vel_threshold: typing.SupportsFloat | typing.SupportsIndex = 5.0, acc_weight: typing.SupportsFloat | typing.SupportsIndex = 0.01, acc_threshold: typing.SupportsFloat | typing.SupportsIndex = 1000.0, print_interval: typing.SupportsInt | typing.SupportsIndex = 1000, crysatilize_interval: typing.SupportsInt | typing.SupportsIndex = 1000) -> tuple[list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]], list[float]]:
        ...
    def __init__(self, seed_points: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]], seed_labels: collections.abc.Sequence[str], seed_timestamp: typing.SupportsFloat | typing.SupportsIndex, seed_index: typing.SupportsInt | typing.SupportsIndex, pairwise_distances: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], pair_weight: typing.SupportsFloat | typing.SupportsIndex = 100.0, pair_threshold: typing.SupportsFloat | typing.SupportsIndex = 0.01, vel_weight: typing.SupportsFloat | typing.SupportsIndex = 1.0, vel_threshold: typing.SupportsFloat | typing.SupportsIndex = 5.0, acc_weight: typing.SupportsFloat | typing.SupportsIndex = 0.01, acc_threshold: typing.SupportsFloat | typing.SupportsIndex = 1000.0) -> None:
        ...
    def crysatilize_beams(self, include_last: bool = True) -> None:
        ...
    def make_next_generation(self, markers: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]], timestamp: typing.SupportsFloat | typing.SupportsIndex, index: typing.SupportsInt | typing.SupportsIndex, trace_head_to_attach: typing.SupportsInt | typing.SupportsIndex, beam_width: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def prune_beams(self, beam_width: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def acc_threshold(self) -> float:
        ...
    @property
    def beams(self) -> list[MultiBeam]:
        ...
    @property
    def pair_weight(self) -> float:
        ...
    @property
    def vel_threshold(self) -> float:
        ...
class MarkerTrace:
    @staticmethod
    def createRawTraces(pointClouds: collections.abc.Sequence[collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]], mergeDistance: typing.SupportsFloat | typing.SupportsIndex = 0.01, mergeFrames: typing.SupportsInt | typing.SupportsIndex = 5) -> list[MarkerTrace]:
        ...
    def appendPoint(self, time: typing.SupportsInt | typing.SupportsIndex, point: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]) -> None:
        """
        Add a point to the end of the marker trace
        """
    def computeBodyMarkerLoss(self, bodyName: str) -> float:
        """
        Each possible combination of (trace, body) can create a marker. This returns a score for a given body, for how "good" of a marker that body would create when combined with this trace. Lower is better.
        """
    def computeBodyMarkerStats(self, skel: _nimblephysics.dynamics.Skeleton, posesOverTime: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]], scalesOverTime: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]]) -> None:
        """
        Each possible combination of (trace, body) can create a marker. So we can compute some summary statistics for each body we could assign this trace to.
        """
    def concat(self, toAppend: MarkerTrace) -> MarkerTrace:
        """
        This merges two MarkerTrace's together, to create a new trace object
        """
    def firstTimestep(self) -> int:
        """
        This returns when this MarkerTrace begins (inclusive)
        """
    def getBestMarker(self) -> tuple[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        """
        This finds the best body to pair this trace with (using the stats from computeBodyMarkerStats()) and returns the best marker
        """
    def lastTimestep(self) -> int:
        """
        This returns when this MarkerTrace ends (inclusive)
        """
    def overlap(self, toAppend: MarkerTrace) -> bool:
        """
        Returns true if these traces overlap in time
        """
    def pointToAppendDistance(self, time: typing.SupportsInt | typing.SupportsIndex, point: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], extrapolate: bool) -> float:
        """
        This gives the distance from the last point (or an extrapolation at this timestep of the last point, of order up to 2)
        """
    @property
    def bodyClosestPointDistance(self) -> dict[str, float]:
        ...
    @property
    def bodyMarkerOffsetVariance(self) -> dict[str, float]:
        ...
    @property
    def bodyMarkerOffsets(self) -> dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @property
    def bodyRootJointDistVariance(self) -> dict[str, float]:
        ...
    @property
    def markerLabel(self) -> str:
        ...
    @property
    def maxTime(self) -> int:
        ...
    @property
    def minTime(self) -> int:
        ...
    @property
    def points(self) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @property
    def times(self) -> list[int]:
        ...
class MarkersErrorReport:
    def getMarkerMapOnTimestep(self, t: typing.SupportsInt | typing.SupportsIndex) -> dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    def getMarkerNamesOnTimestep(self, t: typing.SupportsInt | typing.SupportsIndex) -> list[str]:
        ...
    def getMarkerPositionOnTimestep(self, t: typing.SupportsInt | typing.SupportsIndex, marker: str) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        ...
    def getNumTimesteps(self) -> int:
        ...
    @property
    def droppedMarkerWarnings(self) -> list[list[tuple[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"], str]]]:
        ...
    @droppedMarkerWarnings.setter
    def droppedMarkerWarnings(self, arg0: collections.abc.Sequence[collections.abc.Sequence[tuple[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], str]]]) -> None:
        ...
    @property
    def info(self) -> list[str]:
        ...
    @info.setter
    def info(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
    @property
    def markerObservationsAttemptedFixed(self) -> list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @markerObservationsAttemptedFixed.setter
    def markerObservationsAttemptedFixed(self, arg0: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def markersRenamedFromTo(self) -> list[list[tuple[str, str]]]:
        ...
    @markersRenamedFromTo.setter
    def markersRenamedFromTo(self, arg0: collections.abc.Sequence[collections.abc.Sequence[tuple[str, str]]]) -> None:
        ...
    @property
    def warnings(self) -> list[str]:
        ...
    @warnings.setter
    def warnings(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
class MissingGRFReason:
    """
    Members:
    
      notMissingGRF
    
      measuredGrfZeroWhenAccelerationNonZero
    
      unmeasuredExternalForceDetected
    
      torqueDiscrepancy
    
      forceDiscrepancy
    
      notOverForcePlate
    
      missingImpact
    
      missingBlip
    
      shiftGRF
    
      interpolatedClippedGRF
    
      manualReview
    
      footContactDetectedButNoForce
    
      tooHighMarkerRMS
    
      hasInputOutliers
    
      hasNoForcePlateData
    
      velocitiesStillTooHighAfterFiltering
    
      copOutsideConvexFootError
    
      zeroForceFrame
    
      extendedToNearestPeakForce
    """
    __members__: typing.ClassVar[dict[str, MissingGRFReason]]  # value = {'notMissingGRF': <MissingGRFReason.notMissingGRF: 0>, 'measuredGrfZeroWhenAccelerationNonZero': <MissingGRFReason.measuredGrfZeroWhenAccelerationNonZero: 1>, 'unmeasuredExternalForceDetected': <MissingGRFReason.unmeasuredExternalForceDetected: 2>, 'torqueDiscrepancy': <MissingGRFReason.torqueDiscrepancy: 4>, 'forceDiscrepancy': <MissingGRFReason.forceDiscrepancy: 5>, 'notOverForcePlate': <MissingGRFReason.notOverForcePlate: 6>, 'missingImpact': <MissingGRFReason.missingImpact: 7>, 'missingBlip': <MissingGRFReason.missingBlip: 8>, 'shiftGRF': <MissingGRFReason.shiftGRF: 9>, 'interpolatedClippedGRF': <MissingGRFReason.interpolatedClippedGRF: 11>, 'manualReview': <MissingGRFReason.manualReview: 10>, 'footContactDetectedButNoForce': <MissingGRFReason.footContactDetectedButNoForce: 3>, 'tooHighMarkerRMS': <MissingGRFReason.tooHighMarkerRMS: 12>, 'hasInputOutliers': <MissingGRFReason.hasInputOutliers: 13>, 'hasNoForcePlateData': <MissingGRFReason.hasNoForcePlateData: 14>, 'velocitiesStillTooHighAfterFiltering': <MissingGRFReason.velocitiesStillTooHighAfterFiltering: 15>, 'copOutsideConvexFootError': <MissingGRFReason.copOutsideConvexFootError: 16>, 'zeroForceFrame': <MissingGRFReason.zeroForceFrame: 17>, 'extendedToNearestPeakForce': <MissingGRFReason.extendedToNearestPeakForce: 18>}
    copOutsideConvexFootError: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.copOutsideConvexFootError: 16>
    extendedToNearestPeakForce: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.extendedToNearestPeakForce: 18>
    footContactDetectedButNoForce: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.footContactDetectedButNoForce: 3>
    forceDiscrepancy: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.forceDiscrepancy: 5>
    hasInputOutliers: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.hasInputOutliers: 13>
    hasNoForcePlateData: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.hasNoForcePlateData: 14>
    interpolatedClippedGRF: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.interpolatedClippedGRF: 11>
    manualReview: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.manualReview: 10>
    measuredGrfZeroWhenAccelerationNonZero: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.measuredGrfZeroWhenAccelerationNonZero: 1>
    missingBlip: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.missingBlip: 8>
    missingImpact: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.missingImpact: 7>
    notMissingGRF: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.notMissingGRF: 0>
    notOverForcePlate: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.notOverForcePlate: 6>
    shiftGRF: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.shiftGRF: 9>
    tooHighMarkerRMS: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.tooHighMarkerRMS: 12>
    torqueDiscrepancy: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.torqueDiscrepancy: 4>
    unmeasuredExternalForceDetected: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.unmeasuredExternalForceDetected: 2>
    velocitiesStillTooHighAfterFiltering: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.velocitiesStillTooHighAfterFiltering: 15>
    zeroForceFrame: typing.ClassVar[MissingGRFReason]  # value = <MissingGRFReason.zeroForceFrame: 17>
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
class MissingGRFStatus:
    """
    Members:
    
      no
    
      unknown
    
      yes
    """
    __members__: typing.ClassVar[dict[str, MissingGRFStatus]]  # value = {'no': <MissingGRFStatus.no: 0>, 'unknown': <MissingGRFStatus.unknown: 1>, 'yes': <MissingGRFStatus.yes: 2>}
    no: typing.ClassVar[MissingGRFStatus]  # value = <MissingGRFStatus.no: 0>
    unknown: typing.ClassVar[MissingGRFStatus]  # value = <MissingGRFStatus.unknown: 1>
    yes: typing.ClassVar[MissingGRFStatus]  # value = <MissingGRFStatus.yes: 2>
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
class MultiBeam:
    def __init__(self, cost: typing.SupportsFloat | typing.SupportsIndex, trace_heads: collections.abc.Sequence[TraceHead], timestep_used_markers: collections.abc.Set[str]) -> None:
        ...
    def get_child_trace_heads(self, trace_head: TraceHead, index: typing.SupportsInt | typing.SupportsIndex) -> list[TraceHead]:
        ...
    @property
    def cost(self) -> float:
        ...
    @property
    def timestep_used_markers(self) -> set[str]:
        ...
    @property
    def trace_heads(self) -> list[TraceHead]:
        ...
class NeuralMarkerLabeller(MarkerLabeller):
    def __init__(self, jointCenterPredictor: collections.abc.Callable[[collections.abc.Sequence[collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]], list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]]) -> None:
        ...
class OpenSimFile:
    skeleton: _nimblephysics.dynamics.Skeleton
    def __init__(self, skeleton: _nimblephysics.dynamics.Skeleton, markers: collections.abc.Mapping[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def anatomicalMarkers(self) -> list[str]:
        ...
    @anatomicalMarkers.setter
    def anatomicalMarkers(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
    @property
    def bodyScales(self) -> dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @bodyScales.setter
    def bodyScales(self, arg0: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def ignoredBodies(self) -> list[str]:
        ...
    @ignoredBodies.setter
    def ignoredBodies(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
    @property
    def jointsDrivenBy(self) -> list[tuple[str, str]]:
        ...
    @jointsDrivenBy.setter
    def jointsDrivenBy(self, arg0: collections.abc.Sequence[tuple[str, str]]) -> None:
        ...
    @property
    def markersMap(self) -> dict[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @markersMap.setter
    def markersMap(self, arg0: collections.abc.Mapping[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def meshMap(self) -> dict[str, tuple[str, _nimblephysics.math.Isometry3]]:
        ...
    @meshMap.setter
    def meshMap(self, arg0: collections.abc.Mapping[str, tuple[str, _nimblephysics.math.Isometry3]]) -> None:
        ...
    @property
    def meshScaleMap(self) -> dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @meshScaleMap.setter
    def meshScaleMap(self, arg0: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def trackingMarkers(self) -> list[str]:
        ...
    @trackingMarkers.setter
    def trackingMarkers(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
    @property
    def warnings(self) -> list[str]:
        ...
    @warnings.setter
    def warnings(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
class OpenSimMocoTrajectory:
    @property
    def activationNames(self) -> list[str]:
        ...
    @activationNames.setter
    def activationNames(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
    @property
    def activations(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @activations.setter
    def activations(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def excitationNames(self) -> list[str]:
        ...
    @excitationNames.setter
    def excitationNames(self, arg0: collections.abc.Sequence[str]) -> None:
        ...
    @property
    def excitations(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @excitations.setter
    def excitations(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def timestamps(self) -> list[float]:
        ...
    @timestamps.setter
    def timestamps(self, arg0: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
class OpenSimMot:
    @property
    def poses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    @poses.setter
    def poses(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    @property
    def timestamps(self) -> list[float]:
        ...
    @timestamps.setter
    def timestamps(self, arg0: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
class OpenSimScaleAndMarkerOffsets:
    success: bool
    @property
    def bodyScales(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    @bodyScales.setter
    def bodyScales(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> None:
        ...
    @property
    def markerOffsets(self) -> dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        ...
    @markerOffsets.setter
    def markerOffsets(self, arg0: collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]) -> None:
        ...
    @property
    def markers(self) -> dict[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @markers.setter
    def markers(self, arg0: collections.abc.Mapping[str, tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
class OpenSimTRC:
    @property
    def framesPerSecond(self) -> int:
        ...
    @framesPerSecond.setter
    def framesPerSecond(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def markerLines(self) -> dict[str, list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @markerLines.setter
    def markerLines(self, arg0: collections.abc.Mapping[str, collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def markerTimesteps(self) -> list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    @markerTimesteps.setter
    def markerTimesteps(self, arg0: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    @property
    def timestamps(self) -> list[float]:
        ...
    @timestamps.setter
    def timestamps(self, arg0: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
class ProcessingPassType:
    """
    Members:
    
      KINEMATICS : This is the pass where we solve for kinematics.
    
      DYNAMICS : This is the pass where we solve for dynamics.
    
      LOW_PASS_FILTER : This is the pass where we apply a low-pass filter to the kinematics and dynamics.
    
      ACC_MINIMIZING_FILTER : This is the pass where we apply an acceleration minimizing filter to the kinematics and dynamics.
    """
    ACC_MINIMIZING_FILTER: typing.ClassVar[ProcessingPassType]  # value = <ProcessingPassType.ACC_MINIMIZING_FILTER: 3>
    DYNAMICS: typing.ClassVar[ProcessingPassType]  # value = <ProcessingPassType.DYNAMICS: 1>
    KINEMATICS: typing.ClassVar[ProcessingPassType]  # value = <ProcessingPassType.KINEMATICS: 0>
    LOW_PASS_FILTER: typing.ClassVar[ProcessingPassType]  # value = <ProcessingPassType.LOW_PASS_FILTER: 2>
    __members__: typing.ClassVar[dict[str, ProcessingPassType]]  # value = {'KINEMATICS': <ProcessingPassType.KINEMATICS: 0>, 'DYNAMICS': <ProcessingPassType.DYNAMICS: 1>, 'LOW_PASS_FILTER': <ProcessingPassType.LOW_PASS_FILTER: 2>, 'ACC_MINIMIZING_FILTER': <ProcessingPassType.ACC_MINIMIZING_FILTER: 3>}
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
class ResidualForceHelper:
    def __init__(self, skeleton: _nimblephysics.dynamics.Skeleton, forceBodies: collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex]) -> None:
        ...
    def calculateCOMAngularResidual(self, q: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], dq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], ddq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], forcesConcat: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        This computes the residual at the root, then transforms that to the COM and expresses the torque as a spatial vector (even if the root joint uses euler coordinates for rotation).
        """
    def calculateComToCenterAngularResiduals(self, q: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], dq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], ddq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], forcesConcat: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        """
        This computes the location that we would need to move the COM to in order to center the angular residuals. Moving the COM to the computed location doesn't remove angular residuals, but ensures that any remaining residuals are parallel to the net external force on the body.
        """
    def calculateInverseDynamics(self, q: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], dq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], ddq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], forcesConcat: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def calculateResidual(self, q: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], dq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], ddq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], forcesConcat: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[6, 1]"]:
        ...
    def calculateResidualFreeRootAcceleration(self, q: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], dq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], ddq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], forcesConcat: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[6, 1]"]:
        """
        This computes the acceleration we would need at the root in order to remove all residual forces.
        """
    def calculateResidualJacobianWrt(self, q: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], dq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], ddq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], forcesConcat: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], wrt: _nimblephysics.neural.WithRespectTo) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def calculateResidualNorm(self, q: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], dq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], ddq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], forcesConcat: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], torquesMultiple: typing.SupportsFloat | typing.SupportsIndex, useL1: bool = False) -> float:
        ...
    def calculateResidualNormGradientWrt(self, q: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], dq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], ddq: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], forcesConcat: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"], wrt: _nimblephysics.neural.WithRespectTo, torquesMultiple: typing.SupportsFloat | typing.SupportsIndex, useL1: bool = False) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
class SkeletonConverter:
    def __init__(self, source: _nimblephysics.dynamics.Skeleton, target: _nimblephysics.dynamics.Skeleton) -> None:
        ...
    def convertMotion(self, targetMotion: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], logProgress: bool = True, convergenceThreshold: typing.SupportsFloat | typing.SupportsIndex = 1e-07, maxStepCount: typing.SupportsInt | typing.SupportsIndex = 100, leastSquaresDamping: typing.SupportsFloat | typing.SupportsIndex = 0.01, lineSearch: bool = True, logIKOutput: bool = False) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def createVirtualMarkers(self, addFakeMarkers: typing.SupportsInt | typing.SupportsIndex = 3, weightFakeMarkers: typing.SupportsFloat | typing.SupportsIndex = 0.1) -> None:
        ...
    def debugToGUI(self, gui: ...) -> None:
        ...
    def fitSourceToTarget(self, convergenceThreshold: typing.SupportsFloat | typing.SupportsIndex = 1e-07, maxStepCount: typing.SupportsInt | typing.SupportsIndex = 100, leastSquaresDamping: typing.SupportsFloat | typing.SupportsIndex = 0.01, lineSearch: bool = True, logOutput: bool = False) -> float:
        ...
    def fitTargetToSource(self, convergenceThreshold: typing.SupportsFloat | typing.SupportsIndex = 1e-07, maxStepCount: typing.SupportsInt | typing.SupportsIndex = 100, leastSquaresDamping: typing.SupportsFloat | typing.SupportsIndex = 0.01, lineSearch: bool = True, logOutput: bool = False) -> float:
        ...
    def getSourceJointWorldPositions(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getSourceJoints(self) -> list[_nimblephysics.dynamics.Joint]:
        ...
    def getTargetJointWorldPositions(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 1]"]:
        ...
    def getTargetJoints(self) -> list[_nimblephysics.dynamics.Joint]:
        ...
    def linkJoints(self, sourceJoint: _nimblephysics.dynamics.Joint, targetJoint: _nimblephysics.dynamics.Joint) -> None:
        ...
    def rescaleAndPrepTarget(self, addFakeMarkers: typing.SupportsInt | typing.SupportsIndex = 3, weightFakeMarkers: typing.SupportsFloat | typing.SupportsIndex = 0.1, convergenceThreshold: typing.SupportsFloat | typing.SupportsIndex = 1e-15, maxStepCount: typing.SupportsInt | typing.SupportsIndex = 1000, leastSquaresDamping: typing.SupportsFloat | typing.SupportsIndex = 0.01, lineSearch: bool = True, logOutput: bool = False) -> None:
        ...
class StreamingIK:
    def __init__(self, skeleton: _nimblephysics.dynamics.Skeleton, markers: collections.abc.Sequence[tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    def estimateState(self, now: typing.SupportsInt | typing.SupportsIndex, numHistory: typing.SupportsInt | typing.SupportsIndex = 20, polynomialDegree: typing.SupportsInt | typing.SupportsIndex = 3) -> None:
        ...
    def observeMarkers(self, markers: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]], classes: collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex], timestamp: typing.SupportsInt | typing.SupportsIndex, copTorqueForces: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[9, 1]"]] = []) -> None:
        """
        This method takes in a set of markers, along with their assigned classes, and updates the targets for the IK to match the observed markers.
        """
    def reset(self, arg0: ...) -> None:
        """
        This method allows tests to manually input a set of markers, rather than waiting for Cortex to send them.
        """
    def setAnthropometricPrior(self, prior: Anthropometrics, priorWeight: typing.SupportsFloat | typing.SupportsIndex = 1.0) -> None:
        """
        This sets an anthropometric prior used to help condition the body to keep reasonable scalings.
        """
    def startGUIThread(self, gui: ...) -> None:
        """
        This method starts a thread that periodically updates a GUI server state, though at a much lower framerate than the IK solver.
        """
    def startSolverThread(self) -> None:
        """
        This method starts the thread that runs the IK continuously.
        """
class StreamingMarkerTraces:
    def __init__(self, totalClasses: typing.SupportsInt | typing.SupportsIndex, bufferSize: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def getTraceFeatures(self, numWindows: typing.SupportsInt | typing.SupportsIndex, windowDuration: typing.SupportsInt | typing.SupportsIndex, center: bool = True) -> tuple[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"], typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]]:
        """
        This method returns the features that we used to predict the classes of the markers. The first element of the pair is the features (which are trace points concatenated with the time, as measured in integer units of 'windowDuration', backwards from now), and the second is the trace ID for each point, so that we can correctly assign logit outputs back to the traces.
        """
    def observeMarkers(self, markers: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]], timestamp: typing.SupportsInt | typing.SupportsIndex) -> tuple[list[int], list[int]]:
        """
        This method takes in a set of markers, and returns a vector of the predicted classes for each marker, based on classes we have predicted for previous markers, and continuity assumptions. It also returns a 'trace tag' for each marker, that can be used to associate it with previous continuous observations of the same marker. The returned vector will be the same length and order as the input `markers` vector.
        """
    def observeTraceLogits(self, logits: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], traceIDs: typing.Annotated[numpy.typing.ArrayLike, numpy.int32, "[m, 1]"]) -> None:
        """
        This method takes in the logits for each point, and the trace IDs for each point, and updates the internal state of the trace classifier to reflect the new information.
        """
    def renderTracesToGUI(self, gui: ...) -> None:
        ...
    def reset(self) -> None:
        """
        This resets all traces to empty
        """
    def setFeatureMaxStrideTolerance(self, tolerance: typing.SupportsInt | typing.SupportsIndex) -> None:
        """
        This sets the maximum number of milliseconds that we will tolerate between a stride and a point we are going to accept as being at that stride.
        """
    def setMaxJoinDistance(self, distance: typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
        This method sets the maximum distance that can exist between the last head of a trace, and a new marker position. Markers that are within this distance from a trace are not guaranteed to be merged (they must be the closest to the trace), but markers that are further than this distance are guaranteed to be split into a new trace.
        """
    def setTraceTimeoutMillis(self, timeout: typing.SupportsInt | typing.SupportsIndex) -> None:
        """
        This method sets the timeout for traces. If a trace has not been updated for this many milliseconds, it will be removed from the trace list.
        """
class StreamingMocapLab:
    def __init__(self, skeleton: _nimblephysics.dynamics.Skeleton, markers: collections.abc.Sequence[tuple[_nimblephysics.dynamics.BodyNode, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    def estimateState(self, now: typing.SupportsInt | typing.SupportsIndex, numHistory: typing.SupportsInt | typing.SupportsIndex = 20, polynomialDegree: typing.SupportsInt | typing.SupportsIndex = 3) -> None:
        ...
    def getIK(self) -> StreamingMarkerTraces:
        ...
    def getMarkerTraces(self) -> StreamingMarkerTraces:
        ...
    def getTraceFeatures(self, numWindows: typing.SupportsInt | typing.SupportsIndex, windowDuration: typing.SupportsInt | typing.SupportsIndex) -> tuple[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"], typing.Annotated[numpy.typing.NDArray[numpy.int32], "[m, 1]"]]:
        """
        This method returns the features that we used to predict the classes of the markers. The first element of the pair is the features (which are trace points concatenated with the time, as measured in integer units of 'windowDuration', backwards from now), and the second is the trace ID for each point, so that we can correctly assign logit outputs back to the traces.
        """
    def listenToCortex(self, host: str, cortexMulticastPort: typing.SupportsInt | typing.SupportsIndex = 1001, cortexRequestsPort: typing.SupportsInt | typing.SupportsIndex = 1510) -> None:
        """
        This method establishes a link to Cortex, and listens for real-time observations of markers and force plate data.
        """
    def manuallyObserveMarkers(self, markers: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]], timestamp: typing.SupportsInt | typing.SupportsIndex, copTorqueForces: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[9, 1]"]] = []) -> None:
        """
        This method allows tests to manually input a set of markers, rather than waiting for Cortex to send them.
        """
    def observeTraceLogits(self, logits: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], traceIDs: typing.Annotated[numpy.typing.ArrayLike, numpy.int32, "[m, 1]"]) -> None:
        """
        This method takes in the logits for each point, and the trace IDs for each point, and updates the internal state of the trace classifier to reflect the new information.
        """
    def reset(self, gui: ... = None) -> None:
        """
        This method resets the state of the mocap lab, including the IK and the marker traces.
        """
    def setAnthropometricPrior(self, prior: Anthropometrics, priorWeight: typing.SupportsFloat | typing.SupportsIndex = 1.0) -> None:
        """
        This sets an anthropometric prior used to help condition the body to keep reasonable scalings.
        """
    def startGUIThread(self, gui: ...) -> None:
        """
        This method starts a thread that periodically updates a GUI server state, though at a much lower framerate than the IK solver.
        """
    def startSolverThread(self) -> None:
        """
        This method starts the thread that runs the IK continuously.
        """
class SubjectOnDisk:
    """
    
            This is for doing ML and large-scale data analysis. The idea here is to
            create a lazy-loadable view of a subject, where everything remains on disk
            until asked for. That way we can instantiate thousands of these in memory,
            and not worry about OOM'ing a machine.
          
    """
    @staticmethod
    def writeB3D(path: str, header: SubjectOnDiskHeader) -> None:
        ...
    @typing.overload
    def __init__(self, path: str) -> None:
        ...
    @typing.overload
    def __init__(self, header: SubjectOnDiskHeader) -> None:
        ...
    def getAgeYears(self) -> int:
        """
        This returns the age of the subject, or 0 if unknown.
        """
    def getBiologicalSex(self) -> str:
        """
        This returns a string, one of "male", "female", or "unknown".
        """
    def getCustomValueDim(self, valueName: str) -> int:
        """
        This returns the dimension of the custom value specified by :code:`valueName`
        """
    def getCustomValues(self) -> list[str]:
        """
        A list of all the different types of custom values that this SubjectOnDisk contains. These are unspecified, and are intended to allow an easy extension of the format to unusual types of data (like exoskeleton torques or unusual physical sensors) that may be present on some subjects but not others.
        """
    def getDofAccelerationsFiniteDifferenced(self, trial: typing.SupportsInt | typing.SupportsIndex, processingPass: typing.SupportsInt | typing.SupportsIndex) -> list[bool]:
        """
        This returns the vector of booleans indicating which DOFs have their accelerations from finite-differencing during this trial (as opposed to observed directly through a accelerometer or IMU)
        """
    def getDofPositionsObserved(self, trial: typing.SupportsInt | typing.SupportsIndex, processingPass: typing.SupportsInt | typing.SupportsIndex) -> list[bool]:
        """
        This returns the vector of booleans indicating which DOFs have their positions observed during this trial
        """
    def getDofVelocitiesFiniteDifferenced(self, trial: typing.SupportsInt | typing.SupportsIndex, processingPass: typing.SupportsInt | typing.SupportsIndex) -> list[bool]:
        """
        This returns the vector of booleans indicating which DOFs have their velocities from finite-differencing during this trial (as opposed to observed directly through a gyroscope or IMU)
        """
    def getForcePlateCorners(self, trial: typing.SupportsInt | typing.SupportsIndex, forcePlate: typing.SupportsInt | typing.SupportsIndex) -> list[typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]:
        """
        Get an array of force plate corners (as 3D vectors) for the given force plate in the given trial. Empty array on out-of-bounds access.
        """
    def getForceplateCutoffs(self, trial: typing.SupportsInt | typing.SupportsIndex, processingPass: typing.SupportsInt | typing.SupportsIndex) -> list[float]:
        """
        If we reprocessed the force plates with a cutoff, then these are the cutoff values we used.
        """
    def getGroundForceBodies(self) -> list[str]:
        """
        A list of the :code:`body_name`'s for each body that was assumed to be able to take ground-reaction-force from force plates.
        """
    def getHeaderProto(self) -> SubjectOnDiskHeader:
        """
        This returns the raw proto header for this subject, which can be used to write out a new B3D file
        """
    def getHeightM(self) -> float:
        """
        This returns the height in meters, or 0.0 if unknown.
        """
    def getHref(self) -> str:
        """
        The AddBiomechanics link for this subject's data.
        """
    def getLowpassCutoffFrequency(self, trial: typing.SupportsInt | typing.SupportsIndex, processingPass: typing.SupportsInt | typing.SupportsIndex) -> float:
        """
        If we're doing a lowpass filter on this pass, then what was the cutoff frequency of that (Butterworth) filter?
        """
    def getLowpassFilterOrder(self, trial: typing.SupportsInt | typing.SupportsIndex, processingPass: typing.SupportsInt | typing.SupportsIndex) -> int:
        """
        If we're doing a lowpass filter on this pass, then what was the order of that (Butterworth) filter?
        """
    def getMassKg(self) -> float:
        """
        This returns the mass in kilograms, or 0.0 if unknown.
        """
    def getMissingGRF(self, trial: typing.SupportsInt | typing.SupportsIndex) -> list[MissingGRFReason]:
        """
                    This returns an array of enum values, one per frame in the specified trial,
                    each describing whether physics data can be trusted for the corresponding frame of that trial.
                    
                    Each frame is either `MissingGRFReason.notMissingGRF`, in which case the physics data is probably trustworthy, or
                    some other value indicating why the processing system heuristics believe that there is likely to be unmeasured 
                    external force acting on the body at this time.
        
                    WARNING: If this is true, you can't trust the :code:`tau` or :code:`acc` values on the corresponding frame!!
        
                    This method is provided to give a cheaper way to filter out frames we want to ignore for training, without having to call
                    the more expensive :code:`loadFrames()` and examine frames individually.
        """
    def getNotes(self) -> str:
        """
        The notes (if any) added by the person who uploaded this data to AddBiomechanics.
        """
    def getNumDofs(self) -> int:
        """
        This returns the number of DOFs for the model on this Subject
        """
    def getNumForcePlates(self, trial: typing.SupportsInt | typing.SupportsIndex) -> int:
        """
        The number of force plates in the source data.
        """
    def getNumJoints(self) -> int:
        """
        This returns the number of joints for the model on this Subject
        """
    def getNumProcessingPasses(self) -> int:
        """
        This returns the number of processing passes that were successfully completed on this subject. IMPORTANT: Just because a processing pass was done for the subject does not mean that every trial will have successfully completed that processing pass. For example, some trials may lack force plate data, and thus will not have a dynamics pass that requires force plate data.
        """
    def getNumTrials(self) -> int:
        """
        This returns the number of trials that are in this file.
        """
    def getOpensimFileText(self, processingPass: typing.SupportsInt | typing.SupportsIndex) -> str:
        """
        This will read the raw OpenSim file XML out of the SubjectOnDisk, and return it as a string.
        """
    def getProcessingPassType(self, processingPass: typing.SupportsInt | typing.SupportsIndex) -> ProcessingPassType:
        """
        This returns the type of processing pass at a given index, up to the number of processing passes that were done
        """
    def getQuality(self) -> DataQuality:
        """
        This returns the user-supplied quality of the data in this subject
        """
    def getSubjectTags(self) -> list[str]:
        """
        This returns the list of tags attached to this subject, which are arbitrary strings from the AddBiomechanics platform.
        """
    def getTrialAngularResidualNorms(self, trial: typing.SupportsInt | typing.SupportsIndex, processingPass: typing.SupportsInt | typing.SupportsIndex) -> list[float]:
        """
        This returns the vector of scalars indicating the norm of the root residual torques on each timestep of a given trial
        """
    def getTrialLength(self, trial: typing.SupportsInt | typing.SupportsIndex) -> int:
        """
        This returns the length of the trial requested
        """
    def getTrialLinearResidualNorms(self, trial: typing.SupportsInt | typing.SupportsIndex, processingPass: typing.SupportsInt | typing.SupportsIndex) -> list[float]:
        """
        This returns the vector of scalars indicating the norm of the root residual forces on each timestep of a given trial
        """
    def getTrialMarkerMaxs(self, trial: typing.SupportsInt | typing.SupportsIndex, processingPass: typing.SupportsInt | typing.SupportsIndex) -> list[float]:
        """
        This returns the vector of scalars indicating the max marker error on each timestep of a given trial
        """
    def getTrialMarkerRMSs(self, trial: typing.SupportsInt | typing.SupportsIndex, processingPass: typing.SupportsInt | typing.SupportsIndex) -> list[float]:
        """
        This returns the vector of scalars indicating the RMS marker error on each timestep of a given trial
        """
    def getTrialMaxJointVelocity(self, trial: typing.SupportsInt | typing.SupportsIndex, processingPass: typing.SupportsInt | typing.SupportsIndex) -> list[float]:
        """
        This returns the vector of scalars indicating the maximum absolute velocity of all DOFs on each timestep of a given trial
        """
    def getTrialName(self, trial: typing.SupportsInt | typing.SupportsIndex) -> str:
        """
        This returns the human readable name of the specified trial, given by the person who uploaded the data to AddBiomechanics. This isn't necessary for training, but may be useful for analyzing the data.
        """
    def getTrialNumProcessingPasses(self, trial: typing.SupportsInt | typing.SupportsIndex) -> int:
        """
        This returns the number of processing passes that successfully completed on this trial
        """
    def getTrialOriginalName(self, trial: typing.SupportsInt | typing.SupportsIndex) -> str:
        """
        This returns the original name of the trial before it was (potentially) split into multiple pieces
        """
    def getTrialSplitIndex(self, trial: typing.SupportsInt | typing.SupportsIndex) -> int:
        """
        This returns the index of the split, if this trial was the result of splitting an original trial into multiple pieces
        """
    def getTrialTags(self, trial: typing.SupportsInt | typing.SupportsIndex) -> list[str]:
        """
        This returns the list of tags attached to a given trial index, which are arbitrary strings from the AddBiomechanics platform.
        """
    def getTrialTimestep(self, trial: typing.SupportsInt | typing.SupportsIndex) -> float:
        """
        This returns the timestep size for the trial requested, in seconds per frame
        """
    def hasLoadedAllFrames(self) -> bool:
        """
        This returns true if all the frames have been loaded into memory.
        """
    def loadAllFrames(self, doNotStandardizeForcePlateData: bool = False) -> None:
        """
        This loads all the frames of data, and fills in the processing pass data matrices in the proto header classes.
        """
    def readForcePlates(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> list[ForcePlate]:
        """
        This reads all the raw sensor data for this trial, and constructs force plates.
        """
    def readFrames(self, trial: typing.SupportsInt | typing.SupportsIndex, startFrame: typing.SupportsInt | typing.SupportsIndex, numFramesToRead: typing.SupportsInt | typing.SupportsIndex = 1, includeSensorData: bool = True, includeProcessingPasses: bool = True, stride: typing.SupportsInt | typing.SupportsIndex = 1, contactThreshold: typing.SupportsFloat | typing.SupportsIndex = 1.0) -> FrameList:
        """
        This will read from disk and allocate a number of :code:`Frame` objects. These Frame objects are assumed to be short-lived, to save working memory. For example, you might :code:`readFrames()` to construct a training batch, then immediately allow the frames to go out of scope and be released after the batch backpropagates gradient and loss. On OOB access, prints an error and returns an empty vector.
        """
    def readOpenSimFile(self, processingPass: typing.SupportsInt | typing.SupportsIndex, geometryFolder: str = '', ignoreGeometry: bool = False) -> OpenSimFile:
        """
        This is functionally the same as readSkel(), except that it returns the entire OpenSim file object, which in addition to the Skeleton also contains the markerset.This will read the entire OpenSim file from the binary, and optionally use the passed in :code:`geometryFolder` to load meshes. 
        """
    def readSkel(self, processingPass: typing.SupportsInt | typing.SupportsIndex, geometryFolder: str = '', ignoreGeometry: bool = False) -> _nimblephysics.dynamics.Skeleton:
        """
        This will read the skeleton from the binary, and optionally use the passed in :code:`geometryFolder` to load meshes. We do not bundle meshes with :code:`SubjectOnDisk` files, to save space. If you do not pass in :code:`geometryFolder`, expect to get warnings about being unable to load meshes, and expect that your skeleton will not display if you attempt to visualize it.
        """
class SubjectOnDiskHeader:
    def __init__(self) -> None:
        ...
    def addProcessingPass(self) -> SubjectOnDiskPassHeader:
        ...
    def addTrial(self) -> SubjectOnDiskTrial:
        ...
    def filterTrials(self, keepTrials: collections.abc.Sequence[bool]) -> None:
        ...
    def getProcessingPasses(self) -> list[SubjectOnDiskPassHeader]:
        ...
    def getQuality(self) -> DataQuality:
        ...
    def getTrials(self) -> list[SubjectOnDiskTrial]:
        ...
    def recomputeColumnNames(self) -> None:
        ...
    def setAgeYears(self, ageYears: typing.SupportsInt | typing.SupportsIndex) -> SubjectOnDiskHeader:
        ...
    def setBiologicalSex(self, biologicalSex: str) -> SubjectOnDiskHeader:
        ...
    def setCustomValueNames(self, customValueNames: collections.abc.Sequence[str]) -> SubjectOnDiskHeader:
        ...
    def setGroundForceBodies(self, groundForceBodies: collections.abc.Sequence[str]) -> SubjectOnDiskHeader:
        ...
    def setHeightM(self, heightM: typing.SupportsFloat | typing.SupportsIndex) -> SubjectOnDiskHeader:
        ...
    def setHref(self, sourceHref: str) -> SubjectOnDiskHeader:
        ...
    def setMassKg(self, massKg: typing.SupportsFloat | typing.SupportsIndex) -> SubjectOnDiskHeader:
        ...
    def setNotes(self, notes: str) -> SubjectOnDiskHeader:
        ...
    def setNumDofs(self, dofs: typing.SupportsInt | typing.SupportsIndex) -> SubjectOnDiskHeader:
        ...
    def setNumJoints(self, joints: typing.SupportsInt | typing.SupportsIndex) -> SubjectOnDiskHeader:
        ...
    def setQuality(self, quality: DataQuality) -> SubjectOnDiskHeader:
        ...
    def setSubjectTags(self, subjectTags: collections.abc.Sequence[str]) -> SubjectOnDiskHeader:
        ...
    def setTrials(self, trials: collections.abc.Sequence[SubjectOnDiskTrial]) -> None:
        ...
    def trimToProcessingPasses(self, numPasses: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
class SubjectOnDiskPassHeader:
    def __init__(self) -> None:
        ...
    def getOpenSimFileText(self) -> str:
        ...
    def getProcessingPassType(self) -> ProcessingPassType:
        ...
    def setOpenSimFileText(self, openSimFileText: str) -> None:
        ...
    def setProcessingPassType(self, type: ProcessingPassType) -> None:
        ...
class SubjectOnDiskTrial:
    def __init__(self) -> None:
        ...
    def addPass(self) -> SubjectOnDiskTrialPass:
        """
        This creates a new :code:`SubjectOnDiskTrialPass` for this trial, and returns it. That object can store results from IK and ID, as well as other results from the processing pipeline.
        """
    def getBasicTrialType(self) -> BasicTrialType:
        ...
    def getDetectedTrialFeatures(self) -> list[DetectedTrialFeature]:
        ...
    def getForcePlates(self) -> list[ForcePlate]:
        ...
    def getHasManualGRFAnnotation(self) -> list[bool]:
        ...
    def getMarkerObservations(self) -> list[dict[str, typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]]]:
        ...
    def getMissingGRFReason(self) -> list[MissingGRFReason]:
        ...
    def getName(self) -> str:
        ...
    def getOriginalTrialEndFrame(self) -> int:
        ...
    def getOriginalTrialEndTime(self) -> float:
        ...
    def getOriginalTrialName(self) -> str:
        ...
    def getOriginalTrialStartFrame(self) -> int:
        ...
    def getOriginalTrialStartTime(self) -> float:
        ...
    def getPasses(self) -> list[SubjectOnDiskTrialPass]:
        ...
    def getSplitIndex(self) -> int:
        ...
    def getTimestep(self) -> float:
        ...
    def getTrialLength(self) -> int:
        ...
    def setAccObservations(self, accObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    def setBasicTrialType(self, type: BasicTrialType) -> None:
        ...
    def setCustomValues(self, customValues: collections.abc.Sequence[typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]]) -> None:
        ...
    def setDetectedTrialFeatures(self, features: collections.abc.Sequence[DetectedTrialFeature]) -> None:
        ...
    def setEmgObservations(self, emgObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]]]) -> None:
        ...
    def setExoTorques(self, exoTorques: collections.abc.Mapping[typing.SupportsInt | typing.SupportsIndex, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 1]"]]) -> None:
        ...
    def setForcePlates(self, forcePlates: collections.abc.Sequence[ForcePlate]) -> None:
        ...
    def setGyroObservations(self, gyroObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    def setHasManualGRFAnnotation(self, hasManualGRFAnnotation: collections.abc.Sequence[bool]) -> None:
        ...
    def setMarkerNamesGuessed(self, markersGuessed: bool) -> None:
        ...
    def setMarkerObservations(self, markerObservations: collections.abc.Sequence[collections.abc.Mapping[str, typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"]]]) -> None:
        ...
    def setMissingGRFReason(self, missingGRFReason: collections.abc.Sequence[MissingGRFReason]) -> None:
        ...
    def setName(self, name: str) -> None:
        ...
    def setOriginalTrialEndFrame(self, endFrame: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setOriginalTrialEndTime(self, endTime: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setOriginalTrialName(self, name: str) -> None:
        ...
    def setOriginalTrialStartFrame(self, startFrame: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setOriginalTrialStartTime(self, startTime: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setSplitIndex(self, split: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setTimestep(self, timestep: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setTrialLength(self, length: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setTrialTags(self, trialTags: collections.abc.Sequence[str]) -> None:
        ...
class SubjectOnDiskTrialPass:
    def __init__(self) -> None:
        ...
    def computeKinematicValues(self, skel: _nimblephysics.dynamics.Skeleton, timestep: typing.SupportsFloat | typing.SupportsIndex, poses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], rootHistoryLen: typing.SupportsInt | typing.SupportsIndex = 5, rootHistoryStride: typing.SupportsInt | typing.SupportsIndex = 1, explicitVels: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"] = ..., explicitAccs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"] = ...) -> None:
        ...
    def computeValues(self, skel: _nimblephysics.dynamics.Skeleton, timestep: typing.SupportsFloat | typing.SupportsIndex, poses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], footBodyNames: collections.abc.Sequence[str], forces: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], moments: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], cops: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], rootHistoryLen: typing.SupportsInt | typing.SupportsIndex = 5, rootHistoryStride: typing.SupportsInt | typing.SupportsIndex = 1) -> None:
        ...
    def computeValuesFromForcePlates(self, skel: _nimblephysics.dynamics.Skeleton, timestep: typing.SupportsFloat | typing.SupportsIndex, poses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"], footBodyNames: collections.abc.Sequence[str], forcePlates: collections.abc.Sequence[ForcePlate], rootHistoryLen: typing.SupportsInt | typing.SupportsIndex = 5, rootHistoryStride: typing.SupportsInt | typing.SupportsIndex = 1, explicitVels: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"] = ..., explicitAccs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"] = ..., forcePlateZeroThresholdNewtons: typing.SupportsFloat | typing.SupportsIndex = 3.0) -> None:
        ...
    def copyValuesFrom(self, other: SubjectOnDiskTrialPass) -> None:
        ...
    def getAccs(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getAngularResidual(self) -> list[float]:
        ...
    def getComAccs(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getComAccsInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getComPoses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getComVels(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getGroundBodyCopTorqueForce(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getGroundBodyCopTorqueForceInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getGroundBodyWrenches(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getGroundBodyWrenchesInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getJointCenters(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getJointCentersInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getLinearResidual(self) -> list[float]:
        ...
    def getMarkerMax(self) -> list[float]:
        ...
    def getMarkerRMS(self) -> list[float]:
        ...
    def getPoses(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getProcessedForcePlates(self) -> list[ForcePlate]:
        ...
    def getResamplingMatrix(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getResidualWrenchInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getRootEulerHistoryInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getRootPosHistoryInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getRootSpatialAccInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getRootSpatialVelInRootFrame(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getTaus(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def getType(self) -> ProcessingPassType:
        ...
    def getVels(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, n]"]:
        ...
    def setAccelerationMinimizingForceRegularization(self, reg: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setAccelerationMinimizingRegularization(self, reg: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setAccs(self, accs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setAngularResidual(self, angularResidual: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
    def setComAccs(self, accs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setComAccsInRootFrame(self, accs: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setComPoses(self, poses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setComVels(self, vels: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setDofAccelerationFiniteDifferenced(self, dofAccelerationFiniteDifference: collections.abc.Sequence[bool]) -> None:
        ...
    def setDofPositionsObserved(self, dofPositionsObserved: collections.abc.Sequence[bool]) -> None:
        ...
    def setDofVelocitiesFiniteDifferenced(self, dofVelocitiesFiniteDifferenced: collections.abc.Sequence[bool]) -> None:
        ...
    def setForcePlateCutoffs(self, cutoffs: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
    def setGroundBodyCopTorqueForce(self, copTorqueForces: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setGroundBodyCopTorqueForceInRootFrame(self, copTorqueForces: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setGroundBodyWrenches(self, wrenches: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setGroundBodyWrenchesInRootFrame(self, wrenches: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setJointCenters(self, centers: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setJointCentersInRootFrame(self, centers: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setLinearResidual(self, linearResidual: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
    def setLowpassCutoffFrequency(self, freq: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def setLowpassFilterOrder(self, order: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def setMarkerMax(self, markerMax: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
    def setMarkerRMS(self, markerRMS: collections.abc.Sequence[typing.SupportsFloat | typing.SupportsIndex]) -> None:
        ...
    def setPoses(self, poses: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setResamplingMatrix(self, resamplingMatrix: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setResidualWrenchInRootFrame(self, wrenches: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setRootEulerHistoryInRootFrame(self, rootHistory: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setRootPosHistoryInRootFrame(self, rootHistory: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setRootSpatialAccInRootFrame(self, spatialAcc: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setRootSpatialVelInRootFrame(self, spatialVel: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setTaus(self, taus: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
    def setType(self, type: ProcessingPassType) -> None:
        ...
    def setVels(self, vels: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, n]"]) -> None:
        ...
class TraceHead:
    def __init__(self, label: str, observed_this_timestep: bool, last_observed_point: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], last_observed_timestamp: typing.SupportsFloat | typing.SupportsIndex, last_observed_index: typing.SupportsInt | typing.SupportsIndex, last_observed_velocity: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[3, 1]"], parent: TraceHead = None) -> None:
        ...
    @property
    def label(self) -> str:
        ...
    @property
    def last_observed_index(self) -> int:
        ...
    @property
    def last_observed_point(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        ...
    @property
    def last_observed_timestamp(self) -> float:
        ...
    @property
    def last_observed_velocity(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[3, 1]"]:
        ...
    @property
    def observed_this_timestep(self) -> bool:
        ...
    @property
    def parent(self) -> ...:
        ...
copOutsideConvexFootError: MissingGRFReason  # value = <MissingGRFReason.copOutsideConvexFootError: 16>
extendedToNearestPeakForce: MissingGRFReason  # value = <MissingGRFReason.extendedToNearestPeakForce: 18>
footContactDetectedButNoForce: MissingGRFReason  # value = <MissingGRFReason.footContactDetectedButNoForce: 3>
forceDiscrepancy: MissingGRFReason  # value = <MissingGRFReason.forceDiscrepancy: 5>
hasInputOutliers: MissingGRFReason  # value = <MissingGRFReason.hasInputOutliers: 13>
hasNoForcePlateData: MissingGRFReason  # value = <MissingGRFReason.hasNoForcePlateData: 14>
interpolatedClippedGRF: MissingGRFReason  # value = <MissingGRFReason.interpolatedClippedGRF: 11>
manualReview: MissingGRFReason  # value = <MissingGRFReason.manualReview: 10>
measuredGrfZeroWhenAccelerationNonZero: MissingGRFReason  # value = <MissingGRFReason.measuredGrfZeroWhenAccelerationNonZero: 1>
missingBlip: MissingGRFReason  # value = <MissingGRFReason.missingBlip: 8>
missingImpact: MissingGRFReason  # value = <MissingGRFReason.missingImpact: 7>
no: MissingGRFStatus  # value = <MissingGRFStatus.no: 0>
notMissingGRF: MissingGRFReason  # value = <MissingGRFReason.notMissingGRF: 0>
notOverForcePlate: MissingGRFReason  # value = <MissingGRFReason.notOverForcePlate: 6>
shiftGRF: MissingGRFReason  # value = <MissingGRFReason.shiftGRF: 9>
tooHighMarkerRMS: MissingGRFReason  # value = <MissingGRFReason.tooHighMarkerRMS: 12>
torqueDiscrepancy: MissingGRFReason  # value = <MissingGRFReason.torqueDiscrepancy: 4>
unknown: MissingGRFStatus  # value = <MissingGRFStatus.unknown: 1>
unmeasuredExternalForceDetected: MissingGRFReason  # value = <MissingGRFReason.unmeasuredExternalForceDetected: 2>
velocitiesStillTooHighAfterFiltering: MissingGRFReason  # value = <MissingGRFReason.velocitiesStillTooHighAfterFiltering: 15>
yes: MissingGRFStatus  # value = <MissingGRFStatus.yes: 2>
zeroForceFrame: MissingGRFReason  # value = <MissingGRFReason.zeroForceFrame: 17>
