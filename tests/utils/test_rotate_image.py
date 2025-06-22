import numpy as np

from imgzen import utils
from imgzen._typing import TImage
from tests.utils.fixture import dummy_image


def test_rotate_image(dummy_image: TImage) -> None:
    rotated = utils.rotate_image(dummy_image, angle=90)
    assert rotated.shape == dummy_image.shape
