# test_acceptance_sad.py

from io import BytesIO
import pytest
from app import app

@pytest.fixture
def client():
    """
    Fixture for the Flask test client.
    - Purpose: Set up a test client for making requests to the Flask app during testing.
    - Usage: Provides a `client` object to use for HTTP request simulations.
    """
    with app.test_client() as client:
        yield client

def test_acceptance_missing_file(client):
    """
    Test Case: No File Uploaded
    - Purpose: Validate the application's behavior when no file is provided in the upload request.
    - Scenario:
        - Simulate a POST request to the `/prediction` route with no file data.
        - Assert the response status code is 200 (to indicate a valid request was processed).
        - Verify that the response includes an appropriate error message.
    """
    # Simulate a POST request with no file data
    response = client.post("/prediction", data={}, content_type="multipart/form-data")

    # Assertions:
    # 1. Ensure the response status code is 200, indicating the request was processed.
    assert response.status_code == 200

    # 2. Check for a meaningful error message in the response data.
    #    Modify the message check if your application uses a different error response text.
    assert b"File cannot be processed" in response.data  # Expected error message

# Acceptance Test AT-SAD-004 – Non-image file upload shows user-friendly error
# ---------------------------------------------------------------------------
# GIVEN  the Flask image recognition application is running
#   AND  I can access the home page at "/"
#   AND  I can open the image upload form for /prediction
# WHEN   I first visit the home page
#   AND  then upload a file whose contents are not a valid image (e.g., a text file)
#   AND  submit the form to /prediction
# THEN   the server responds with HTTP 200 OK
#   AND  the result page displays the error message "File cannot be processed."
#   AND  no valid digit Prediction is shown for the uploaded file
def test_acceptance_non_image_upload_shows_error(client):
    """
    AT-SAD-002:
    Full user flow (home -> upload) where the user selects a non-image file.
    The system should not crash; it should show the "File cannot be processed."
    error message on the result page.
    """
    # Step 1: User visits the home page (GET "/")
    home_response = client.get("/")
    assert home_response.status_code == 200

    # Step 2: User selects a non-image (corrupt) file in the upload form
    corrupt_file = BytesIO(b"this is definitely not an image file")
    corrupt_file.name = "notes.txt"

    # Step 3: User submits the form to /prediction
    response = client.post(
        "/prediction",
        data={"file": (corrupt_file, corrupt_file.name)},
        content_type="multipart/form-data",
    )

    # Step 4: Behaviour-level assertions
    assert response.status_code == 200
    # app.py catches processing errors and renders result.html with this exact message
    assert b"File cannot be processed." in response.data
