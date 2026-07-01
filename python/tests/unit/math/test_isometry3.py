import numpy as np

import dartpy as dart


def test_multiply_numpy_array():
    transform = dart.math.Isometry3()
    assert np.allclose(transform.multiply(np.array([0, 0, 0])), [0, 0, 0])


if __name__ == "__main__":
    test_multiply_numpy_array()
