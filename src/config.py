BASE_URL = "https://restful-booker.herokuapp.com"

USERNAME = "admin"
PASSWORD = "password123"

TIMEOUT = 5

BOOKING_SCHEMA = {
    "type": "object",
    "properties": {
        "bookingid": {
            "type": "number"
        },
        "booking": {
            "type": "object",
            "properties": {
                "firstname": {
                    "type": "string"
                },
                "lastname": {
                    "type": "string"
                },
                "totalprice": {
                    "type": "number"
                },
                "depositpaid": {
                    "type": "boolean"
                },
                "bookingdates": {
                    "type": "object",
                    "properties": {
                        "checkin": {
                            "type": "string",
                            "format": "date"
                        },
                        "checkout": {
                            "type": "string",
                            "format": "date"
                        }
                    },
                    "required": ["checkin", "checkout"]
                },
                "additionalneeds": {
                    "type": "string"
                }
            },
            "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]
        }
    },
    "required": ["bookingid", "booking"]
}

