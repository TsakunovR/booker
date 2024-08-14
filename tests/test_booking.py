import pytest
import requests


def test_ping(api_client):
    status_code = api_client.ping()

    assert status_code == 201


def test_create_booking(create_and_verify_booking):
    response = create_and_verify_booking()

    assert response["bookingid"] is not None


def test_filter_by_created_booking(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    filter_response = api_client.get_booking_ids()

    assert any(b['bookingid'] == booking_id for b in filter_response)


def test_filter_by_name_created_booking(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']
    params = {
        "firstname": "Jango",
        "lastname": "Freedom"
    }
    filter_response = api_client.get_booking_ids(params=params)

    assert any(b['bookingid'] == booking_id for b in filter_response)


# def test_filter_by_checkin_checkout_created_booking(api_client, create_booking):
#     response = create_booking()
#     booking_id = response['bookingid']
#     params = {
#         "checkin": "2024-10-15",
#         "checkout": "2024-10-20"
#     }
#     filter_response = api_client.get_booking_ids(params=params)
#     print("Booking ID:", booking_id)
#     print("Filter Response:", filter_response)
#
#     assert any(b['bookingid'] == booking_id for b in filter_response)


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


@pytest.mark.no_cleanup
def test_delete_booking(api_client, create_and_verify_booking):
    response = create_and_verify_booking()
    booking_id = response['bookingid']

    delete_success = api_client.delete_booking(booking_id)

    assert delete_success

    with pytest.raises(requests.exceptions.HTTPError):
        api_client.get_booking_by_id(booking_id)
