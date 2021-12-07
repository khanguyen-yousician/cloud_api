from typing import Optional

import pydantic
from pydantic import Field

from packages.aiven_api import cloud as cloud_api
from packages.aiven_api.models import cloud as cloud_model
from flask_pydantic import validate

from apps.api import api


@api.route('/cloud_providers')
@validate()
def get_cloud_providers() -> cloud_model.CloudProviderResponse:
    cloud_providers = cloud_api.get_all_cloud_providers()
    return cloud_providers


@api.route('/regions')
@validate()
def get_regions() -> cloud_model.SupportRegionResponse:
    supported_regions = cloud_api.get_supported_regions()
    return supported_regions


@api.route('/clouds')
@validate()
def get_clouds(query: cloud_model.GetCloudsInput) -> cloud_model.CloudResponse:
    clouds = cloud_api.get_all_clouds(query)
    return clouds
