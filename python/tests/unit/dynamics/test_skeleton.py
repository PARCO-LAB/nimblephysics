import platform
import pytest
import numpy as np
import dartpy as dart


def test_basic():
    skel = dart.dynamics.Skeleton()

    joint_prop = dart.dynamics.FreeJointProperties()
    joint_prop.mName = 'joint0'
    assert joint_prop.mName == 'joint0'

    [joint1, body1] = skel.createFreeJointAndBodyNodePair(None, joint_prop)
    assert joint1.getType() == 'FreeJoint'
    assert joint1.getName() == 'joint0'


def test_set_body_scales():
    skel = dart.dynamics.Skeleton()
    skel.createFreeJointAndBodyNodePair()

    scales = np.array([1.25, 0.75, 1.5])
    skel.setBodyScales(scales)
    assert np.allclose(skel.getBodyScales(), scales)


if __name__ == "__main__":
    pytest.main()
