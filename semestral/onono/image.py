import PIL.Image
import numpy as np
from PIL import Image, ImageOps
from pathlib import Path


def load_image(name: str, dims: tuple = (10, 10), percent_filled: float = 0.7):
    """
    Loads an image from the `saves/images` directory, performs various operations and returns it as an array.
    In case something goes wrong, returns None.
    """
    name += ".png"
    path = Path(__file__).parent.parent
    path = (path / 'saves/images' / name).resolve()
    try:
        image = Image.open(path)
        image = ImageOps.grayscale(image)
        image = ImageOps.fit(image, dims)
        image = np.asarray(image)
        image = apply_threshold(image, percent_filled)
        return image
    except (FileNotFoundError, ValueError):
        return None


def apply_threshold(image: np.ndarray, expected_filled: float = 0.7):
    """
    Takes an image and an expected ratio of ones in a matrix. Finds the optimal threshold that puts the real ratio
    closest to the expected one. Returns the matrix after threshold is applied.
    """
    total_px = image.shape[0] * image.shape[1]

    threshold = 128
    closest_match = 1.
    while True:
        mask = image > threshold
        filled = mask.sum() / total_px
        difference = filled - expected_filled

        if threshold == 128 or abs(difference) <= closest_match:
            closest_match = abs(difference)
        else:
            break

        if difference < 0:
            threshold -= 1
        else:
            threshold += 1

    # print(f"Threshold {threshold}, {filled * 100:.1f} % filled")
    return mask
