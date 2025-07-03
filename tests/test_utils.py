from imgzen import utils

from tests.utils.fixture import dummy_image
from imgzen._typing import TImage


def test_enhance_contrast(dummy_image: TImage) -> None:
    contrasted = utils.enhance_contrast(dummy_image)
    assert contrasted.shape == dummy_image.shape


def test_blur_background(dummy_image: TImage) -> None:
    blurred_image = utils.blur_background(dummy_image)
    assert blurred_image.shape == dummy_image.shape


def test_auto_correction(dummy_image: TImage) -> None:
    corrected = utils.auto_correction(dummy_image)
    assert corrected.shape == dummy_image.shape
