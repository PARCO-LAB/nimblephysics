import platform
import pytest
import numpy as np
import dartpy as dart


def test_empty_world():
    world = dart.simulation.World('my world')
    assert world.getNumSkeletons() is 0
    assert world.getNumSimpleFrames() is 0


def test_collision_detector_change():
    world = dart.simulation.World('world')
    solver = world.getConstraintSolver()
    assert solver is not None

    assert solver.getCollisionDetector().getType() == dart.collision.FCLCollisionDetector().getStaticType()

    solver.setCollisionDetector(dart.collision.DARTCollisionDetector())
    assert solver.getCollisionDetector().getType() == dart.collision.DARTCollisionDetector().getStaticType()

    if hasattr(dart.collision, 'BulletCollisionDetector'):
        solver.setCollisionDetector(dart.collision.BulletCollisionDetector())
        assert solver.getCollisionDetector().getType() == dart.collision.BulletCollisionDetector().getStaticType()

    if hasattr(dart.collision, 'OdeCollisionDetector'):
        solver.setCollisionDetector(dart.collision.OdeCollisionDetector())
        assert solver.getCollisionDetector().getType() == dart.collision.OdeCollisionDetector().getStaticType()


def test_set_positions():
    world = dart.simulation.World('world')
    skel = dart.dynamics.Skeleton()
    skel.createFreeJointAndBodyNodePair()
    world.addSkeleton(skel)

    positions = np.arange(world.getNumDofs(), dtype=float)
    world.setPositions(positions)
    assert np.allclose(world.getPositions(), positions)


def test_set_velocities_and_gravity():
    world = dart.simulation.World('world')
    skel = dart.dynamics.Skeleton()
    skel.createFreeJointAndBodyNodePair()
    world.addSkeleton(skel)

    velocities = np.arange(world.getNumDofs(), dtype=float)
    gravity = np.array([0.0, -9.81, 0.0])

    world.setVelocities(velocities)
    world.setGravity(gravity)

    assert np.allclose(world.getVelocities(), velocities)
    assert np.allclose(world.getGravity(), gravity)


if __name__ == "__main__":
    pytest.main()
