import pathlib

import nimblephysics as nimble
import torch


def main():
    world = nimble.loadWorld(str(pathlib.Path(__file__).resolve().parents[2] / "data" / "skel" / "half_cheetah.skel"))
    initial_state = torch.zeros((world.getStateSize(),))
    action = torch.zeros((world.getActionSize(),))

    state = initial_state
    for _ in range(5):
        state = nimble.timestep(world, state, action)

    assert state.shape[0] == world.getStateSize()
    return state


if __name__ == "__main__":
    main()
