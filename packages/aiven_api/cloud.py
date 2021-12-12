import requests

from packages.aiven_api import constants
from packages.aiven_api.models import cloud as cloud_model
from packages.cache import cache
from geopy.distance import distance

from packages.exceptions.exceptions import AivenApiException


def extract_cloud_provider(cloud_name: str) -> str:
    return cloud_name.split('-')[0]


@cache.cached(timeout=60 * 60, query_string=True)
def get_all_clouds(
        query: cloud_model.GetCloudsInput
) -> cloud_model.CloudResponse:

    response = requests.get(constants.CLOUD_API_URL).json()
    if 'errors' in response:
        raise AivenApiException("Aiven Api errors", 400)

    all_clouds = cloud_model.CloudResponse(**response)

    if query.region:
        print(f'region = {query.region.value}')
        all_clouds.clouds = [
            filtered_cloud for filtered_cloud in all_clouds.clouds
            if filtered_cloud.geo_region == query.region.value
        ]

    if query.provider:
        all_clouds.clouds = [
            filtered_cloud for filtered_cloud in all_clouds.clouds
            if extract_cloud_provider(filtered_cloud.cloud_name) == query.provider.value
        ]

    if query.longitude is not None and query.latitude is not None:
        all_clouds.clouds.sort(key=lambda x: distance(
            [query.latitude, query.longitude],
            [x.geo_latitude, x.geo_longitude])
        )
    return all_clouds


def get_all_cloud_providers() -> cloud_model.CloudProviderResponse:
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
    return cloud_model.CloudProviderResponse(**cloud_providers)


def get_supported_regions() -> cloud_model.SupportRegionResponse:
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

    return cloud_model.SupportRegionResponse(**supported_regions)
