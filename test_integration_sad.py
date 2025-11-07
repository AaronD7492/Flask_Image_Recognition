# test_integration_sad.py

import pytest
from app import app
from io import BytesIO

@pytest.fixture
def client():
    """Fixture for the Flask test client."""
    with app.test_client() as client:
        yield client

def test_missing_file(client):
    """Test the prediction route with a missing file."""
    response = client.post("/prediction", data={}, content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"File cannot be processed." in response.data  # Check if the error message is displayed

def test_invalid_file_type(client):
    """Test the prediction route with an invalid file type."""
    invalid_file = BytesIO(b"This is not an image file.")
    invalid_file.name = "test.txt"

    response = client.post(
        "/prediction",
        data={"file": (invalid_file, invalid_file.name)},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"File cannot be processed." in response.data  # Check if the error message is displayed
