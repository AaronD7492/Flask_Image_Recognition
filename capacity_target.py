"""
Capacity test target for Locust.

This uses the real image-preprocessing pipeline from model.py and
a synthetic "inference-like" numeric workload.

We intentionally avoid calling the TensorFlow model directly because
its concurrency behaviour is unstable under Locust-style load, which
is outside the scope of this course.

Locust will repeatedly call compute_capacity_value(), and we can
increase EXPANSION to simulate a heavier workload (similar idea to
the Fibonacci example from the activity).
"""

from pathlib import Path

import numpy as np

from model import preprocess_img

# Use the same image you mentioned:
# test_images / "1" / "Sign 1 (8).jpeg"
TEST_IMAGE_PATH = (
    Path(__file__).parent / "test_images" / "1" / "Sign 1 (8).jpeg"
)

# Expansion factor: number of "inference-like" loops per call
EXPANSION = 1


def compute_capacity_value() -> float:
    """
    Load and preprocess the sample image, then perform a numeric
    workload EXPANSION times to simulate inference cost.

    Returns a float (aggregate of the computations) so the function
    is not optimized away.
    """
    # Real preprocessing from your project
    img_array = preprocess_img(TEST_IMAGE_PATH)  # shape should be (1, 224, 224, 3) or similar

    # Synthetic "inference-like" numeric workload
    # (repeat EXPANSION times so we can scale the work)
    result = 0.0
    for _ in range(EXPANSION):
        # Example: mean + simple transformation
        m = float(np.mean(img_array))
        result += m * m

    return result


if __name__ == "__main__":
    # Quick manual test
    print("Capacity test result:", compute_capacity_value())
