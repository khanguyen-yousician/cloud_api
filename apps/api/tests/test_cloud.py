import unittest
from unittest import mock

from app import app
from packages.exceptions.exceptions import AivenApiException


class TestCloudApi(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @mock.patch('packages.aiven_api.cloud.get_all_clouds')
    def test_fetch_clouds(self, aiven_mock):
        sample_response = {
            'clouds': [
                {
                    "cloud_description": "Europe, Finland - UpCloud: Helsinki",
                    "cloud_name": "upcloud-fi-hel",
                    "geo_latitude": 60.17,
                    "geo_longitude": 24.97,
                    "geo_region": "europe"
                }
            ]
        }

        aiven_mock.return_value = sample_response
        assert self.client.get('/clouds').json == sample_response

        sample_response = {
            'clouds': [
                {
                    "cloud_description": "Europe, Finland - UpCloud: Helsinki",
                    "cloud_name": "upcloud-fi-hel",
                    "geo_latitude": 60.17,
                    "geo_longitude": 24.97,
                    "geo_region": "europe"
                },
                {
                    "cloud_description": "Asia, Bahrain - Amazon Web Services: Bahrain",
                    "cloud_name": "aws-me-south-1",
                    "geo_latitude": 26.07,
                    "geo_longitude": 50.55,
                    "geo_region": "south asia"
                }
            ]
        }

        aiven_mock.return_value = sample_response
        region = 'invalid'
        response = self.client.get(f'/clouds?region={region}')
        assert response.status_code == 400

        provider = 'invalid'
        response = self.client.get(f'/clouds?provider={provider}')
        assert response.status_code == 400

        provider = 'aws'
        response = self.client.get(f'/clouds?provider={provider}')
        assert response.status_code == 200

        response = self.client.get(f'/clouds?latitude={50}')
        assert response.status_code == 400

        response = self.client.get(f'/clouds?longitude={50}')
        assert response.status_code == 400

        response = self.client.get(f'/clouds?latitude={50}&longitude={50}')
        assert response.status_code == 200

    @mock.patch('packages.aiven_api.cloud.get_all_clouds')
    def test_fetch_clouds_exception(self, aiven_mock):
        aiven_mock.side_effect = AivenApiException("Aiven Api errors", 400)
        response = self.client.get('/clouds')
        assert response.status_code == 400

    @mock.patch('requests.get')
    def test_fetch_cloud_providers(self, request_mock):
        cloud_providers = {
            'providers': [
                {
                    'code': 'aws',
                    'name': 'Amazon Web Services'
                },
                {
                    'code': 'azure',
                    'name': 'Microsoft Azure Cloud'
                },
                {
                    'code': 'google',
                    'name': 'Google Cloud'
                },
                {
                    'code': 'do',
                    'name': 'Digital Ocean'
                },
                {
                    'code': 'upcloud',
                    'name': 'UpCloud'
                }
            ]
        }
        response = self.client.get(f'/cloud_providers')
        assert response.json == cloud_providers


    def test_fetch_cloud_regions(self):
        supported_regions = {
            'supported_regions': [
                'africa',
                'australia',
                'east asia',
                'europe',
                'middle east',
                'north america',
                'south america',
                'south asia',
                'southeast asia'
            ]
        }

        response = self.client.get(f'/regions')
        assert response.json == supported_regions


if __name__ == "__main__":
    unittest.main()
