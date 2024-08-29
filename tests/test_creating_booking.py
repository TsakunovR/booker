import allure


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking')
def test_create_booking_positive(create_and_verify_booking):
    response = create_and_verify_booking()

    assert response["bookingid"] is not None


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(create_and_verify_booking):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }
    response = create_and_verify_booking(booking_data, use_fixed_dates=False)
    booking = response["booking"]

    assert booking["firstname"] == booking_data["firstname"]
    assert booking["lastname"] == booking_data["lastname"]
    assert booking["totalprice"] == booking_data["totalprice"]
    assert booking["depositpaid"] == booking_data["depositpaid"]
    assert response["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]
    assert booking["additionalneeds"] == booking_data["additionalneeds"]


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking only with required fields')
def test_create_booking_missing_required_fields(create_partial_booking):
    booking_data = {
        "firstname": "Bob",
        "lastname": "Builder",
        "totalprice": 100,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2025-03-01",
            "checkout": "2025-03-05"
        }
    }
    response = create_partial_booking(booking_data)
    booking = response["booking"]

    assert booking["firstname"] == booking_data["firstname"]
    assert booking["lastname"] == booking_data["lastname"]
    assert booking["totalprice"] == booking_data["totalprice"]
    assert booking["depositpaid"] == booking_data["depositpaid"]
    assert booking["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert booking["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]
    assert booking["additionalneeds"] is not None


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with other date format')
def test_create_booking_invalid_date_format(create_and_verify_booking, convert_date_format):
    booking_data_incorrect = {
        "bookingdates": {
            "checkin": "01-01-2025",
            "checkout": "02-02-2025"
        }
    }

    response = create_and_verify_booking(booking_data_incorrect, ignore_data_check=True)
    booking = response["booking"]
    expected_checkin_date = convert_date_format(booking_data_incorrect["bookingdates"]["checkin"])
    expected_checkout_date = convert_date_format(booking_data_incorrect["bookingdates"]["checkout"])

    assert booking["bookingdates"]["checkin"] == expected_checkin_date, (
        f"Expected checkin date {expected_checkin_date}, but got {booking['bookingdates']['checkin']}"
    )
    assert booking["bookingdates"]["checkout"] == expected_checkout_date, (
        f"Expected checkout date {expected_checkout_date}, but got {booking['bookingdates']['checkout']}"
    )


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with different date format')
def test_create_booking_with_different_data_format(create_and_verify_booking, convert_date_format):
    booking_data_incorrect = {
        "bookingdates": {
            "checkin": "01-01-2025",
            "checkout": "2025-01-25"
        }
    }

    response = create_and_verify_booking(booking_data_incorrect, ignore_data_check=True)
    booking = response["booking"]
    expected_checkin_date = convert_date_format(booking_data_incorrect["bookingdates"]["checkin"])

    assert booking["bookingdates"]["checkin"] == expected_checkin_date, (
        f"Expected checkin date {expected_checkin_date}, but got {booking['bookingdates']['checkin']}"
    )
    assert booking["bookingdates"]["checkout"] == booking_data_incorrect["bookingdates"]["checkout"]


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with one field')
def test_create_booking_missing_required_fields(create_partial_booking):
    incomplete_data = {
        "firstname": "Tom"
    }
    response = create_partial_booking(incomplete_data)

    assert response["status_code"] == 500
    assert "Internal Server Error" in response["error_message"]


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with invalid data types')
def test_create_booking_invalid_data_types(create_partial_booking):
    invalid_data = {
        "lastname": 10,
        "totalprice": "сто двадцать",
        "depositpaid": "Да",
        "bookingdates": {
            "checkin": "2025-04-01",
            "checkout": "2025-04-10"
        },
        "additionalneeds": None
    }
    response = create_partial_booking(invalid_data)

    assert response["status_code"] == 500
    assert "Internal Server Error" in response["error_message"]


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with incorrect date format')
def test_create_booking_with_different_data_format(create_and_verify_booking):
    booking_data_incorrect = {
        "bookingdates": {
            "checkin": "",
            "checkout": True
        }
    }

    response = create_and_verify_booking(booking_data_incorrect, ignore_data_check=True)
    booking = response["booking"]

    assert booking["bookingdates"]["checkin"] == "0NaN-aN-aN"
    assert booking["bookingdates"]["checkout"] == "1970-01-01"
