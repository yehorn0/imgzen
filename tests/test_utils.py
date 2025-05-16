import numpy as np
import pytest

from picflow import utils


@pytest.fixture
def mock_image():
    return np.full((100, 100, 3), 128, dtype=np.uint8)


def test_rotate_image(mock_image):
    rotated_image = utils.rotate_image(mock_image)
    assert rotated_image.shape == mock_image.shape

