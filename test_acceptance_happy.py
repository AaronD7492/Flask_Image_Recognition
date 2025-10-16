# test_acceptance_happy.py

from io import BytesIO
import pytest

def test_acceptance_successful_upload(client):
    """
    Test Case: Successful Upload of a Valid Image File
    - Purpose: Ensure the application accepts a valid image file upload and provides a prediction.
    - Method:
        - Create a mock valid image file with minimal valid data.
        - Simulate a POST request to the `/prediction` route with the file.
        - Assert the response status code is 200.
        - Verify that the response data includes the keyword 'Prediction.'
    """
    img_data = BytesIO(b"fake_image_data")  # Simulated valid image data
    img_data.name = "test_image.jpg"

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"Prediction" in response.data


def test_acceptance_valid_large_image(client):
    """
    Test Case: Upload of a Valid Large Image File
    - Purpose: Check if the system accepts large but valid image files without errors and still provides predictions.
    - Method:
        - Create a mock large image file by repeating mock image data multiple times.
        - Simulate a POST request to the `/prediction` route with the file.
        - Assert the response status code is 200.
        - Verify the presence of 'Prediction' in the response data.
    """
    img_data = BytesIO(b"fake_large_image_data" * 1000)  # Simulating a large image
    img_data.name = "large_image.jpg"

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"Prediction" in response.data


def test_acceptance_valid_image_size_upload(client):
    """
    Test Case: Upload of an Image with a Specific Large Size
    - Purpose: Validate system behavior with valid image files of a specific size or resolution.
    - Method:
        - Simulate an image upload with mock data representing a large image.
        - POST the file to the `/prediction` route.
        - Check that the status code is 200 and 'Prediction' exists in the response.
    """
    img_data = BytesIO(b"valid_image_data_of_large_size" * 1000)  # Simulating a specific size
    img_data.name = "large_image.jpg"

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"Prediction" in response.data

def test_acceptance_various_extensions(client):
    """
    Test Case: Upload of Images with Various Valid Extensions
    - Purpose: Ensure the system correctly processes images with different valid file extensions.
    - Method:
        - Create mock image files with various common extensions (e.g., .png, .jpeg, .bmp).
        - Simulate POST requests to the `/prediction` route for each file.
        - Assert that each response has a status code of 200 and contains 'Prediction.'
    """
    valid_extensions = ["test_image.png", "test_image.jpeg", "test_image.bmp"]
    for ext in valid_extensions:
        img_data = BytesIO(b"valid_image_data")
        img_data.name = ext

        response = client.post(
            "/prediction",
            data={"file": (img_data, img_data.name)},
            content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert b"Prediction" in response.data

def test_acceptance_various_image_formats(client):
    """
    Test Case: Upload of Images in Various Formats
    - Purpose: Verify that the system can handle different image formats (e.g., RGB, Grayscale).
    - Method:
        - Create mock image files representing different formats.
        - Simulate POST requests to the `/prediction` route for each format.
        - Assert that each response has a status code of 200 and contains 'Prediction.'
    """
    image_formats = ["rgb_image.jpg", "grayscale_image.jpg"]
    for fmt in image_formats:
        img_data = BytesIO(b"valid_image_data_for_" + fmt.encode())
        img_data.name = fmt

        response = client.post(
            "/prediction",
            data={"file": (img_data, img_data.name)},
            content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert b"Prediction" in response.data
