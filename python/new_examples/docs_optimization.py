import nimblephysics as nimble
import numpy as np


def main():
    model = nimble.models.RajagopalHumanBodyModel()
    skeleton = model.skeleton
    wrist = skeleton.getJoint("radius_hand_r")
    target = np.array([0.5, 0.5, 0.5])

    wrist_pos = skeleton.getJointWorldPositions([wrist])
    error = wrist_pos - target
    loss = np.inner(error, error)

    assert wrist_pos.shape == (3,)
    assert loss >= 0.0
    return loss


if __name__ == "__main__":
    main()
