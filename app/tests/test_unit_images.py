import pytest


def test_image_upload(client):
    response = client.post(
        "/api/v1/images/",
        files={"file": ("fakeimage.jpg", b"image data")},
    )
    assert response.status_code == 200
    assert response.json() == {"image": "fakeimage.jpg"}