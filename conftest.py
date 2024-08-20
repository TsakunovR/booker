import pytest
from src.api_client import APIClient
from src.api_client_no_auth import APIClientNoAuth
from jsonschema import validate, ValidationError
from src.config import BOOKING_SCHEMA
import allure
from requests.exceptions import HTTPError
from datetime import datetime


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
        return response, data

    no_cleanup = request.node.get_closest_marker('no_cleanup')
    if not no_cleanup:
        yield _create_booking
        for booking_id in created_bookings:
            api_client.delete_booking(booking_id)
    else:
        yield _create_booking


@pytest.fixture(scope="function")
def create_and_verify_booking(create_booking):
    def _create_and_verify_booking(booking_data_override=None, ignore_data_check=False):
        response, original_data = create_booking(booking_data_override)
        booking_data = response["booking"]
        try:
            with allure.step('Checking json schema'):
                validate(instance=response, schema=BOOKING_SCHEMA)
        except ValidationError as e:
            pytest.fail(f"JSON schema validation failed: {e.message}")

        assert booking_data["firstname"] == original_data["firstname"]
        assert booking_data["lastname"] == original_data["lastname"]
        assert booking_data["totalprice"] == original_data["totalprice"]
        assert booking_data["depositpaid"] == original_data["depositpaid"]
        if not ignore_data_check:
            assert booking_data["bookingdates"]["checkin"] == original_data["bookingdates"]["checkin"]
            assert booking_data["bookingdates"]["checkout"] == original_data["bookingdates"]["checkout"]
        assert booking_data["additionalneeds"] == original_data["additionalneeds"]

        return response

    return _create_and_verify_booking


@pytest.fixture(scope="function")
def create_partial_booking(api_client, request):
    created_bookings = []

    def _create_partial_booking(booking_data):
        try:
            response = api_client.create_booking(booking_data)
            created_bookings.append(response.get('bookingid'))
            return response
        except HTTPError as e:
            return {
                "status_code": e.response.status_code,
                "error_message": e.response.text
            }

    no_cleanup = request.node.get_closest_marker('no_cleanup')
    if not no_cleanup:
        yield _create_partial_booking
        for booking_id in created_bookings:
            if booking_id:
                api_client.delete_booking(booking_id)
    else:
        yield _create_partial_booking


@pytest.fixture
def convert_date_format():
    def _convert_date_format(date_str):
        try:
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            return date_obj.strftime('%Y-%d-%m')
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}")

    return _convert_date_format


@pytest.fixture()
def api_client_no_auth():
    return APIClientNoAuth()
