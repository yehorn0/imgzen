from imgzen import utils
from imgzen._typing import TImage
from tests.utils.fixture import dummy_image


def test_resize_image(dummy_image: TImage) -> None:
    resized = utils.resize_image(dummy_image, width=50)
    assert resized.shape[1] == 50


def test_resize_image_no_sizes(dummy_image: TImage) -> None:
    resized = utils.resize_image(dummy_image)
    assert resized.shape == dummy_image.shape
