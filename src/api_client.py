import requests
from src.config import BASE_URL, USERNAME, PASSWORD, TIMEOUT
from src.endpoints import AUTH_ENDPOINT, BOOKING_ENDPOINT
from requests.auth import HTTPBasicAuth
import allure


class APIClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()

    def ping(self):
        with allure.step('Ping api client'):
            url = f"{self.base_url}/ping"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"
        return response.status_code

    def authenticate(self):
        with allure.step('Getting authenticate'):
            url = f"{self.base_url}{AUTH_ENDPOINT}"
            payload = {"username": USERNAME, "password": PASSWORD}
            response = self.session.post(url, json=payload, timeout=TIMEOUT)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        token = response.json().get("token")
        with allure.step('Updating header with authorization'):
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def create_booking(self, booking_data):
        with allure.step('Creating booking'):
            url = f"{self.base_url}{BOOKING_ENDPOINT}"
            response = self.session.post(url, json=booking_data)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        return response.json()

    def get_booking_ids(self, params=None):
        with allure.step('Getting object with bookings'):
            url = f"{self.base_url}{BOOKING_ENDPOINT}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        return response.json()

    def get_booking_by_id(self, booking_id):
        with allure.step('Getting object with bookings by id'):
            url = f"{self.base_url}{BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        return response.json()

    def update_booking(self, booking_id, updated_data):
        with allure.step('Updating booking'):
            url = f"{self.base_url}{BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.put(url, json=updated_data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        # print(f"PUT URL: {url}")
        # print(f"Data: {updated_data}")
        # print(f"Response Status Code: {response.status_code}")
        # print(f"Response Content: {response.text}")
        # print(f"Headers: {self.session.headers}")
        response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        return response.json()

    def patch_booking(self, booking_id, part_of_updated_data):
        with allure.step('Patching booking'):
            url = f"{self.base_url}{BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.patch(url, json=part_of_updated_data, auth=HTTPBasicAuth(USERNAME, PASSWORD))
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        return {
            "status_code": response.status_code,
            "json": response.json()
        }

    def delete_booking(self, booking_id):
        with allure.step('Deleting booking'):
            url = f"{self.base_url}/booking/{booking_id}"
            response = self.session.delete(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"
        return response.status_code == 201

