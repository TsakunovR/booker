import pytest
from src.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    client.authenticate()
    return client


@pytest.fixture(scope="function")
def create_booking(api_client):
    booking_data = {
        "firstname": "Jango",
        "lastname": "Freedom",
        "totalprice": 120,
        "depositpaid": True,
        "bookingdates": {
        "checkin": "2024-10-15",
        "checkout": "2024-10-20"
            },
        "additionalneeds": "Breakfast"
    }

    def _create_booking(booking_data_override=None):
        data = {**booking_data, **(booking_data_override or {})}
        response = api_client.create_booking(data)
        return response

    return _create_booking

# @pytest.fixture(scope="function")
# def create_booking(api_client):
#     def _create_booking(booking_data):
#         response = api_client.create_booking(booking_data)
#         return response
#     return _create_booking
