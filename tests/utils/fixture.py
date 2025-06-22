from typing import Any

import numpy as np
import pytest


@pytest.fixture  # type: ignore[misc, unused-ignore]
def dummy_image() -> Any:
    return np.full((100, 100, 3), 128, dtype=np.uint8)
