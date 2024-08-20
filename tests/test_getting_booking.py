import allure
import pytest


@allure.feature('Test getting booking')
@allure.story('Positive: getting booking from list of bookings')
def test_filter_by_created_booking(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    filter_response = api_client.get_booking_ids()

    assert any(b['bookingid'] == booking_id for b in filter_response)


@allure.feature('Test getting booking')
@allure.story('Positive: filter by name created booking')
def test_filter_by_name_created_booking(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    params = {
        "firstname": "Jango",
        "lastname": "Freedom"
    }
    filter_response = api_client.get_booking_ids(params=params)

    assert any(b['bookingid'] == booking_id for b in filter_response)


@allure.feature('Test getting booking')
@allure.story('Positive: filter by booking dates, range is correct')
def test_filter_by_checkin_checkout_created_booking(api_client, create_booking):
    response, _ = create_booking()
    booking_id = response['bookingid']
    params = {
        "checkin": "2024-10-10",
        "checkout": "2024-10-30"
    }
    filter_response = api_client.get_booking_ids(params=params)

    assert any(b['bookingid'] == booking_id for b in filter_response)


@allure.feature('Test getting booking')
@allure.story('Positive: filter by booking ID')
def test_get_booking_by_id(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_data = response['booking']
    booking_id = response['bookingid']

    booking_response = api_client.get_booking_by_id(booking_id)

    assert booking_response['firstname'] == booking_data['firstname']
    assert booking_response['lastname'] == booking_data['lastname']
    assert booking_response['totalprice'] == booking_data['totalprice']
    assert booking_response['depositpaid'] == booking_data['depositpaid']
    assert booking_response['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert booking_response['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert booking_response['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test getting booking')
@allure.story('Negative: getting non-existent booking by ID')
def test_get_nonexistent_booking_by_id(api_client):
    nonexistent_booking_id = 99999999999999
    with pytest.raises(Exception) as excinfo:
        api_client.get_booking_by_id(nonexistent_booking_id)

    assert "Not Found" in str(excinfo.value)


@allure.feature('Test getting booking')
@allure.story('Negative: filter by nonexistent name')
def test_filter_by_nonexistent_name(api_client):
    params = {
        "firstname": "NonExistentFirstName",
        "lastname": "NonExistentLastName"
    }
    filter_response = api_client.get_booking_ids(params=params)

    assert len(filter_response) == 0


@allure.feature('Test getting booking')
@allure.story('Negative: filtering by incorrect date range')
def test_filter_by_incorrect_date_range(api_client):
    params = {
        "checkin": "5050-01-01",
        "checkout": "5050-12-31"
    }
    filter_response = api_client.get_booking_ids(params=params)

    assert len(filter_response) == 0


@allure.feature('Test getting booking')
@allure.story('Negative: getting booking with invalid ID format')
def test_get_booking_with_invalid_id_format(api_client):
    invalid_booking_id = "invalid_id"
    with pytest.raises(Exception) as excinfo:
        api_client.get_booking_by_id(invalid_booking_id)

    assert "404 Client Error: Not Found for url: " in str(excinfo.value)


@allure.feature('Test getting booking')
@allure.story('Negative: filtering without empty parameters')
def test_filter_without_empty_parameters(api_client):
    params = {
        "firstname": "",
        "lastname": ""
    }
    filter_response = api_client.get_booking_ids(params=params)

    assert len(filter_response) == 0


@allure.feature('Test getting booking')
@allure.story('Negative: filtering with bookingdates in created booking')
def test_filter_by_checkin_checkout_of_created_booking(api_client, create_booking):
    response, _ = create_booking()
    params = {
        "checkin": "2024-10-15",
        "checkout": "2024-10-20"
    }
    filter_response = api_client.get_booking_ids(params=params)

    assert len(filter_response) == 0

