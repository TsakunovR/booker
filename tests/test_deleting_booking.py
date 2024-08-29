import pytest
import requests
import allure


@pytest.mark.no_cleanup
@allure.feature('Test deleting booking')
@allure.story('Positive: deleting booking')
def test_delete_booking(api_client, create_and_verify_booking):
    response = create_and_verify_booking(use_fixed_dates=False)
    booking_id = response['bookingid']

    print(response)

    delete_success = api_client.delete_booking(booking_id)

    assert delete_success

    with pytest.raises(requests.exceptions.HTTPError):
        api_client.get_booking_by_id(booking_id)


@allure.feature('Test deleting booking')
@allure.story('Negative: deleting non-existent booking')
def test_delete_non_existent_booking(api_client):
    non_existent_booking_id = 9999999999

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.delete_booking(non_existent_booking_id)

    assert exc_info.value.response.status_code == 405


@allure.feature('Test deleting booking')
@allure.story('Negative: deleting booking without authorization')
def test_delete_booking_without_authorization(api_client_no_auth, create_and_verify_booking):
    response = create_and_verify_booking(use_fixed_dates=False)
    booking_id = response['bookingid']

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client_no_auth.delete_booking(booking_id)

    assert exc_info.value.response.status_code == 403


@allure.feature('Test deleting booking')
@allure.story('Negative: deleting booking with invalid ID')
def test_delete_booking_with_invalid_id(api_client):
    invalid_booking_id = "invalid_id"

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.delete_booking(invalid_booking_id)

    assert exc_info.value.response.status_code == 405


@allure.feature('Test deleting booking')
@allure.story('Negative: deleting booking already deleted')
@pytest.mark.no_cleanup
def test_delete_booking_already_deleted(api_client, create_and_verify_booking):
    response = create_and_verify_booking(use_fixed_dates=False)
    booking_id = response['bookingid']

    delete_success = api_client.delete_booking(booking_id)
    assert delete_success
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.delete_booking(booking_id)

    assert exc_info.value.response.status_code == 405

