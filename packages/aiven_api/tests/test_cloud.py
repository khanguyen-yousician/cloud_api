import unittest
from unittest import mock

import responses

from app import app
from packages.aiven_api import cloud, constants
from packages.aiven_api.models import cloud as cloud_model


class TestAivenApi(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @mock.patch('requests.get')
    def test_fetch_clouds(self, request_mock):
        sample_response = {
            "clouds": [
                {
                    "cloud_description": "Europe, Finland - UpCloud: Helsinki",
                    "cloud_name": "upcloud-fi-hel",
                    "geo_latitude": 60.17,
                    "geo_longitude": 24.97,
                    "geo_region": "europe"
                },
                {
                    "cloud_description": "Europe, Finland - Google Cloud: Finland",
                    "cloud_name": "google-europe-north1",
                    "geo_latitude": 60.5693,
                    "geo_longitude": 27.1878,
                    "geo_region": "europe"
                },
            ]
        }
        request_mock.return_value.status_code.return_value = 200
        request_mock.return_value.json.return_value = sample_response
        responses.add(responses.GET, constants.CLOUD_API_URL, )
        query = cloud_model.GetCloudsInput()
        cloud_resp = cloud.get_all_clouds(query)
        assert cloud_resp == cloud_model.CloudResponse(**sample_response)

    @mock.patch('requests.get')
    def test_fetch_clouds_with_query(self, request_mock):
        aws_cloud_sa = {
            "cloud_description": "South America, Brazil - Amazon Web Services: São Paulo",
            "cloud_name": "aws-sa-east-1",
            "geo_latitude": -23.55,
            "geo_longitude": -46.63,
            "geo_region": "south america"
        }
        aws_cloud_africa = {
            "cloud_description": "Africa, South Africa - Amazon Web Services: Cape Town",
            "cloud_name": "aws-af-south-1",
            "geo_latitude": -33.92,
            "geo_longitude": 18.42,
            "geo_region": "africa"
        }
        azure_cloud_africa = {
            "cloud_description": "Africa, South Africa - Azure: South Africa North",
            "cloud_name": "azure-south-africa-north",
            "geo_latitude": -26.198,
            "geo_longitude": 28.03,
            "geo_region": "africa"
        }
        sample_response = {
            "clouds": [
                aws_cloud_sa,
                aws_cloud_africa,
                azure_cloud_africa,
            ]
        }
        request_mock.return_value.status_code.return_value = 200
        request_mock.return_value.json.return_value = sample_response

        # Test provider filter
        query = cloud_model.GetCloudsInput(provider='aws')
        expected_result = {
            "clouds": [
                aws_cloud_sa,
                aws_cloud_africa
            ]
        }
        cloud_resp = cloud.get_all_clouds(query)
        assert cloud_resp == cloud_model.CloudResponse(**expected_result)

        # Test region filter
        query = cloud_model.GetCloudsInput(region='africa')
        expected_result = {
            "clouds": [
                aws_cloud_africa,
                azure_cloud_africa,
            ]
        }
        cloud_resp = cloud.get_all_clouds(query)
        assert cloud_resp == cloud_model.CloudResponse(**expected_result)

        # Test sort by location
        query = cloud_model.GetCloudsInput(latitude=-26.198, longitude=28.03)
        expected_result = {
            "clouds": [
                azure_cloud_africa,
                aws_cloud_africa,
                aws_cloud_sa
            ]
        }
        cloud_resp = cloud.get_all_clouds(query)
        assert cloud_resp == cloud_model.CloudResponse(**expected_result)


if __name__ == "__main__":
    unittest.main()
