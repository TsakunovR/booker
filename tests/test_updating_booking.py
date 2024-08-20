import allure
import requests
import pytest


@allure.feature('Test updating booking')
@allure.story('Positive: updating booking')
def test_update_booking(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    updated_data = {
        "firstname": "John",
        "lastname": "Dory",
        "totalprice": 111,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-06"
        },
        "additionalneeds": "Lunch"
    }

    api_client.authenticate()
    api_client.update_booking(booking_id, updated_data)
    booking_response = api_client.get_booking_by_id(booking_id)

    assert booking_response['firstname'] == updated_data['firstname']
    assert booking_response['lastname'] == updated_data['lastname']
    assert booking_response['totalprice'] == updated_data['totalprice']
    assert booking_response['depositpaid'] == updated_data['depositpaid']
    assert booking_response['bookingdates']['checkin'] == updated_data['bookingdates']['checkin']
    assert booking_response['bookingdates']['checkout'] == updated_data['bookingdates']['checkout']
    assert booking_response['additionalneeds'] == updated_data['additionalneeds']


@allure.feature('Test updating booking')
@allure.story('Negative: updating booking without authorization')
def test_update_booking_without_authorization(api_client_no_auth, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    updated_data = {
        "firstname": "Unauthorized",
        "lastname": "User",
        "totalprice": 999,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-06"
        },
        "additionalneeds": "None"
    }
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client_no_auth.update_booking(booking_id, updated_data)

    assert exc_info.value.response.status_code == 403, f"Expected status 403 but got {exc_info.value.response.status_code}"


@allure.feature('Test updating booking')
@allure.story('Negative: updating booking with non-existent field')
def test_update_booking_with_non_existent_field(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    invalid_field_data = {
        "non_existent_field": "InvalidData",
        "firstname": "Jane"
    }
    api_client.authenticate()
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.update_booking(booking_id, invalid_field_data)

    assert exc_info.value.response.status_code == 400, f"Expected status 400 but got {exc_info.value.response.status_code}"


@allure.feature('Test updating booking')
@allure.story('Negative: updating booking with invalid data')
def test_update_booking_with_invalid_data(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    invalid_data = {
        "firstname": 123,
        "lastname": True,
        "totalprice": "abc",
        "bookingdates": {
            "checkin": "InvalidDate",
            "checkout": "InvalidDate"
        }
    }
    api_client.authenticate()
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.update_booking(booking_id, invalid_data)

    assert exc_info.value.response.status_code == 500, f"Expected status 500 but got {exc_info.value.response.status_code}"


@allure.feature('Test updating booking')
@allure.story('Negative: updating non-existent booking')
def test_update_non_existent_booking(api_client):
    non_existent_booking_id = 9999999999
    updated_data = {
        "firstname": "Ghost",
        "lastname": "User",
        "totalprice": 555,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-03-01",
            "checkout": "2025-03-06"
        },
        "additionalneeds": "None"
    }

    api_client.authenticate()
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.update_booking(non_existent_booking_id, updated_data)
    assert exc_info.value.response.status_code == 405, f"Expected status 405 but got {exc_info.value.response.status_code}"





