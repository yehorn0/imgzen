import sys
import numpy as np
import pytest
import cv2
import imgzen.utils as utils
from imgzen.main import main
from unittest import mock


@pytest.fixture
def dummy_image():
    return np.ones((10, 10, 3), dtype=np.uint8)


@pytest.fixture
def patch_utils(dummy_image):
    with (
        mock.patch.object(utils, "rotate_image", return_value=dummy_image) as m_rotate,
        mock.patch.object(utils, "resize_image", return_value=dummy_image) as m_resize,
        mock.patch.object(utils, "enhance_contrast", return_value=dummy_image) as m_contrast,
        mock.patch.object(utils, "blur_background", return_value=dummy_image) as m_blur,
        mock.patch.object(utils, "auto_correction", return_value=dummy_image) as m_autocorrect,
    ):
        yield {
            "rotate": m_rotate,
            "resize": m_resize,
            "contrast": m_contrast,
            "blur": m_blur,
            "autocorrect": m_autocorrect,
        }


@pytest.fixture
def patch_cv2(dummy_image):
    with (
        mock.patch("cv2.imread", return_value=dummy_image) as m_imread,
        mock.patch("cv2.imwrite", return_value=True) as m_imwrite,
    ):
        yield m_imread, m_imwrite


@pytest.fixture
def patch_os_makedirs():
    with mock.patch("os.makedirs") as m:
        yield m


def test_rotate_command(monkeypatch, patch_utils, patch_cv2, patch_os_makedirs, tmp_path):
    input_path = tmp_path / "in.jpg"
    output_path = tmp_path / "out.jpg"
    input_path.write_bytes(b"dummy")

    monkeypatch.setattr(
        sys, "argv", ["cli.py", "rotate", "-i", str(input_path), "-o", str(output_path), "-a", "45"]
    )

    main()

    patch_utils["rotate"].assert_called_once()
    args, kwargs = patch_utils["rotate"].call_args
    assert isinstance(args[0], np.ndarray)
    assert args[1] == 45 or kwargs.get("angle") == 45

    _, imwrite = patch_cv2
    imwrite.assert_called_once_with(str(output_path), mock.ANY)


def test_resize_command(monkeypatch, patch_utils, patch_cv2, patch_os_makedirs, tmp_path):
    input_path = tmp_path / "in.jpg"
    output_path = tmp_path / "out.jpg"
    input_path.write_bytes(b"dummy")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cli.py",
            "resize",
            "-i",
            str(input_path),
            "-o",
            str(output_path),
            "--width",
            "200",
            "--height",
            "100",
        ],
    )

    main()

    patch_utils["resize"].assert_called_once_with(mock.ANY, width=200, height=100)

    _, imwrite = patch_cv2
    imwrite.assert_called_once_with(str(output_path), mock.ANY)


def test_contrast_command(monkeypatch, patch_utils, patch_cv2, patch_os_makedirs, tmp_path):
    input_path = tmp_path / "in.jpg"
    output_path = tmp_path / "out.jpg"
    input_path.write_bytes(b"dummy")

    monkeypatch.setattr(sys, "argv", ["cli.py", "contrast", "-i", str(input_path), "-o", str(output_path)])

    main()

    patch_utils["contrast"].assert_called_once_with(mock.ANY)
    _, imwrite = patch_cv2
    imwrite.assert_called_once_with(str(output_path), mock.ANY)


def test_blur_command(monkeypatch, patch_utils, patch_cv2, patch_os_makedirs, tmp_path):
    input_path = tmp_path / "in.jpg"
    output_path = tmp_path / "out.jpg"
    input_path.write_bytes(b"dummy")

    monkeypatch.setattr(
        sys, "argv", ["cli.py", "blur", "-i", str(input_path), "-o", str(output_path), "-k", "25"]
    )

    main()

    patch_utils["blur"].assert_called_once_with(mock.ANY, kernel=(25, 25))
    _, imwrite = patch_cv2
    imwrite.assert_called_once_with(str(output_path), mock.ANY)


def test_autocorrect_command(monkeypatch, patch_utils, patch_cv2, patch_os_makedirs, tmp_path):
    input_path = tmp_path / "in.jpg"
    output_path = tmp_path / "out.jpg"
    input_path.write_bytes(b"dummy")

    monkeypatch.setattr(
        sys, "argv", ["cli.py", "autocorrect", "-i", str(input_path), "-o", str(output_path)]
    )

    main()

    patch_utils["autocorrect"].assert_called_once_with(mock.ANY)
    _, imwrite = patch_cv2
    imwrite.assert_called_once_with(str(output_path), mock.ANY)


def test_image_not_found(monkeypatch, patch_cv2, capsys, tmp_path):
    m_imread, _ = patch_cv2
    m_imread.return_value = None

    input_path = tmp_path / "missing.jpg"
    output_path = tmp_path / "out.jpg"

    monkeypatch.setattr(sys, "argv", ["cli.py", "rotate", "-i", str(input_path), "-o", str(output_path)])

    main()

    captured = capsys.readouterr()
    assert f"Image not found at {input_path}" in captured.out
