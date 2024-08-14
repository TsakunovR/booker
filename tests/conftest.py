import pytest
from src.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    client.authenticate()
    return client


@pytest.fixture(scope="function")
def create_booking(api_client, request):
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
    created_bookings = []

    def _create_booking(booking_data_override=None):
        data = {**booking_data, **(booking_data_override or {})}
        response = api_client.create_booking(data)
        created_bookings.append(response['bookingid'])
        return response

    no_cleanup = request.node.get_closest_marker('no_cleanup')
    if not no_cleanup:
        yield _create_booking
        for booking_id in created_bookings:
            api_client.delete_booking(booking_id)
    else:
        yield _create_booking


@pytest.fixture(scope="function")
def create_and_verify_booking(create_booking):
    def _create_and_verify_booking(booking_data_override=None):
        response = create_booking(booking_data_override)
        booking_data = response["booking"]

        assert booking_data["firstname"] == "Jango"
        assert booking_data["lastname"] == "Freedom"
        assert booking_data["totalprice"] == 120
        assert booking_data["depositpaid"] is True
        assert booking_data["bookingdates"]["checkin"] == "2024-10-15"
        assert booking_data["bookingdates"]["checkout"] == "2024-10-20"
        assert booking_data["additionalneeds"] == "Breakfast"

        return response

    return _create_and_verify_booking

# @pytest.fixture(scope="function")
# def create_booking(api_client):
#     def _create_booking(booking_data):
#         response = api_client.create_booking(booking_data)
#         return response
#     return _create_booking
