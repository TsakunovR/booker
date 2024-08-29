import requests
from src.config import configurations
from src.endpoints import BOOKING_ENDPOINT
import allure


class APIClientNoAuth:
    def __init__(self, environment='development'):
        self.config = configurations.get(environment, configurations['development'])
        self.base_url = self.config.BASE_URL
        self.session = requests.Session()

    def delete_booking(self, booking_id):
        with allure.step('Deleting booking'):
            url = f"{self.base_url}{BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.delete(url)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"
        return response.status_code == 201

    def update_booking(self, booking_id, updated_data):
        with allure.step('Updating booking without authorization'):
            url = f"{self.base_url}{BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.put(url, json=updated_data)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        return response.json()

    def patch_booking(self, booking_id, updated_data):
        with allure.step('Patching booking'):
            url = f"{self.base_url}{BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.patch(url, json=updated_data)
            if not response.ok:
                response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        return response.json()
