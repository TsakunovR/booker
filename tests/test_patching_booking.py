import allure
import requests
import pytest


@allure.feature('Test patching booking')
@allure.story('Positive: patching booking')
def test_update_part_of_booking(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    not_update_data = response['booking']

    part_of_updated_data = {
        "firstname": "Johnatten",
        "lastname": "Doryan"
    }

    api_client.authenticate()

    api_client.patch_booking(booking_id, part_of_updated_data)
    booking_response = api_client.get_booking_by_id(booking_id)

    assert booking_response['firstname'] == part_of_updated_data['firstname']
    assert booking_response['lastname'] == part_of_updated_data['lastname']
    assert booking_response['totalprice'] == not_update_data['totalprice']
    assert booking_response['depositpaid'] == not_update_data['depositpaid']
    assert booking_response['bookingdates']['checkin'] == not_update_data['bookingdates']['checkin']
    assert booking_response['bookingdates']['checkout'] == not_update_data['bookingdates']['checkout']
    assert booking_response['additionalneeds'] == not_update_data['additionalneeds']


@allure.feature('Test patching booking')
@allure.story('Positive: patching booking with partially invalid data')
def test_patch_booking_with_partially_invalid_data(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    not_update_data = response['booking']
    part_of_updated_invalid_data = {
        "firstname": "",
        "lastname": "РАРАРАРА",
        "bookingdates": {
        "checkin": 6454,
            },
        "additionalneeds": False
    }
    api_client.authenticate()
    api_client.patch_booking(booking_id, part_of_updated_invalid_data)
    booking_response = api_client.get_booking_by_id(booking_id)

    assert booking_response['firstname'] == part_of_updated_invalid_data['firstname']
    assert booking_response['lastname'] == part_of_updated_invalid_data['lastname']
    assert booking_response['totalprice'] == not_update_data['totalprice']
    assert booking_response['depositpaid'] == not_update_data['depositpaid']
    assert booking_response['bookingdates']['checkin'] == '1970-01-01'
    assert booking_response['bookingdates']['checkout'] == '0NaN-aN-aN'
    assert booking_response['additionalneeds'] == part_of_updated_invalid_data['additionalneeds']


@allure.feature('Test patching booking')
@allure.story('Negative: patching booking without authorization')
def test_patch_booking_without_authorization(api_client_no_auth, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    part_of_updated_data = {
        "firstname": "Unauthorized",
        "lastname": "User"
    }
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client_no_auth.patch_booking(booking_id, part_of_updated_data)

    assert exc_info.value.response.status_code == 403


@allure.feature('Test patching booking')
@allure.story('Negative: patching non-existent booking')
def test_patch_non_existent_booking(api_client, create_and_verify_booking):
    create_and_verify_booking()
    non_existent_booking_id = 9999999999
    part_of_updated_data = {
        "firstname": "John",
        "lastname": "Doe"
    }
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.patch_booking(non_existent_booking_id, part_of_updated_data)

    assert exc_info.value.response.status_code == 405


@allure.feature('Test patching booking')
@allure.story('Negative: patching booking with non-existent field')
def test_patch_booking_with_non_existent_field(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    invalid_field_data = {
        "non_existent_field": "SomeValue"
    }
    api_client.authenticate()
    response = api_client.patch_booking(booking_id, invalid_field_data)

    assert response['status_code'] == 200
    assert "non_existent_field" not in response['json']
