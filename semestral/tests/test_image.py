from pathlib import Path

import numpy as np
import pytest

import onono.image


@pytest.mark.parametrize('name, dims, valid',
                         [("lenna", (10, 10), True),
                          ("lenny", (10, 10), True),
                          ("lenna", (600, 600), False),
                          ("lenny", (600, 600), True),
                          ("tests/invalid1", (10, 10), False),
                          ("tests/miluju_progtest", (10, 10), False)])
def test_load_image(name, dims, valid):
    img = onono.image.load_image(name, dims)

    if valid:
        assert isinstance(img, np.ndarray)
        assert img.ndim == 2
        assert img.shape == dims

        for row in img:
            for x in row:
                assert x in [0, 1]
    else:
        assert img is None


def get_ratio(img: np.ndarray) -> float:
    """
    Helper function for test_apply_threshold. Calculates ratio of ones in array.
    """
    total = img.shape[0] * img.shape[1]
    filled = img.sum()

    return filled / total


@pytest.mark.parametrize('name',
                         ["lenna.png", "lenny.png", "cvut.png"])
def test_apply_threshold(name: str):
    path = Path(__file__).parent.parent
    path = (path / 'saves' / 'images' / name).resolve()
    img = onono.image.image_prepare(path, (10, 10))

    assert isinstance(onono.image.apply_threshold(img, 0.5, True), tuple)
    assert isinstance(onono.image.apply_threshold(img, 0.5, False), np.ndarray)

    prev_threshold = 255  # maximum value
    prev_ratio = 0.
    for expected_ratio in np.arange(0, 1.1, 0.1):
        mask, threshold = onono.image.apply_threshold(img, expected_ratio, True)
        ratio = get_ratio(mask)

        assert threshold <= prev_threshold and ratio >= prev_ratio
        print(f"Threshold {threshold:03d}, ratio {ratio:.4f}")

        prev_threshold, prev_ratio = threshold, ratio


def test_get_images():
    assert len(onono.image.get_images()) >= 3  # 3 currently used, more can be added later
