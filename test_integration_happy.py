# test_integration_happy.py

from io import BytesIO
import pytest

def test_successful_prediction(client):
    """Test the successful image upload and prediction."""
    # Create a mock image file with minimal valid content
    img_data = BytesIO(b"fake_image_data")
    img_data.name = "test.jpg"

    # Simulate a file upload to the correct prediction endpoint
    response = client.post(
        "/prediction",  # Correct route for prediction
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

    # Assertions
    assert response.status_code == 200
    assert b"Prediction" in response.data  # Modify this check based on your output

def test_prediction_happy_valid_png(client):
    """Happy path: upload a valid-looking PNG and expect a prediction result."""
    img_data = BytesIO(b"fake_png_image_data")
    img_data.name = "test_png.png"

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"Prediction" in response.data
