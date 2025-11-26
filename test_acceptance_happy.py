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

# Acceptance Test AT-HAPPY-EXT-001 – Upload images with different valid extensions
# ------------------------------------------------------------------------------
# GIVEN  the Flask Image Recognition application is running
#        I can access the home page at "/"
#        I have several image files with different valid extensions (.png, .jpeg, .bmp)
# WHEN   I visit the home page
#        upload each of these images through the prediction form
# THEN   the server responds with HTTP 200 OK for each file
#        each result page displays a Prediction for the uploaded image
def test_acceptance_various_extensions(client):
    valid_extensions = ["test_image.png", "test_image.jpeg", "test_image.bmp"]

    # Step 1: User visits home page
    home_response = client.get("/")
    assert home_response.status_code == 200

    # Step 2: User uploads each file type
    for ext in valid_extensions:
        img_data = BytesIO(b"valid_image_data")
        img_data.name = ext

        response = client.post(
            "/prediction",
            data={"file": (img_data, img_data.name)},
            content_type="multipart/form-data"
        )

        # Step 3: Behaviour-level checks
        assert response.status_code == 200
        assert b"Prediction" in response.data

# Acceptance Test AT-HAPPY-FMT-002 – Upload images representing various formats
# ------------------------------------------------------------------------------
# GIVEN  the Flask Image Recognition application is running
#        I can access the home page at "/"
#        I have images representing different formats (RGB, Grayscale)
# WHEN   I visit the home page
#        upload each formatted image through the prediction form
# THEN   the server responds with HTTP 200 OK for each file
#        each result page displays a Prediction for the uploaded image
def test_acceptance_various_image_formats(client):
    image_formats = ["rgb_image.jpg", "grayscale_image.jpg"]

    # Step 1: User visits home page
    home_response = client.get("/")
    assert home_response.status_code == 200

    # Step 2: User uploads images with different formats
    for fmt in image_formats:
        img_data = BytesIO(b"valid_image_data_for_" + fmt.encode())
        img_data.name = fmt

        response = client.post(
            "/prediction",
            data={"file": (img_data, img_data.name)},
            content_type="multipart/form-data"
        )

        # Step 3: Behaviour checks
        assert response.status_code == 200
        assert b"Prediction" in response.data

# Acceptance Test AT-HAPPY-TRANSPARENT-003 – Upload image with transparent background
# ----------------------------------------------------------------------------------
# GIVEN  the Flask Image Recognition application is running
#   AND  I can access the home page at "/"
#   AND  I have an image with a transparent background
# WHEN   I visit the home page
#   AND  upload this image through the prediction form
# THEN   the server responds with HTTP 200 OK
#   AND  the result page displays a Prediction for the uploaded image
def test_acceptance_valid_transparent_background(client):
    # Step 1: User visits home page
    home_response = client.get("/")
    assert home_response.status_code == 200

    # Step 2: User uploads transparent-background image
    img_data = BytesIO(b"valid_image_data_Transparent_Background" * 500)
    img_data.name = "transparent_background_image.png"

    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )

    # Step 3: Behaviour checks
    assert response.status_code == 200
    assert b"Prediction" in response.data
