from io import BytesIO
from typing import Union

import cv2
import numpy as np
from PIL import Image


def read_image_as_pil(file: Union[bytes, "UploadedFile"]) -> Image.Image:
    """
    Read an uploaded file (Streamlit UploadedFile or raw bytes) as a PIL Image,
    ensuring it is in RGB format. Uses OpenCV for robustness if needed.
    """
    if hasattr(file, "read"):
        data = file.read()
    else:
        data = file

    image = Image.open(BytesIO(data))

    if image.mode != "RGB":
        image = image.convert("RGB")

    return image


def pil_to_opencv(image: Image.Image) -> np.ndarray:
    """
    Convert a PIL Image (RGB) to an OpenCV BGR array.
    Useful if future processing steps rely on OpenCV.
    """
    rgb = np.array(image)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    return bgr


def resize_for_display(image: Image.Image, max_size: int = 800) -> Image.Image:
    """
    Resize image to a maximum edge length while preserving aspect ratio.
    """
    w, h = image.size
    scale = min(max_size / max(w, h), 1.0)
    if scale < 1.0:
        new_w = int(w * scale)
        new_h = int(h * scale)
        image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    return image

