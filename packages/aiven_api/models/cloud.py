from enum import Enum
from typing import List, Optional, Any, Dict

import pydantic


class CloudResponse(pydantic.BaseModel):
    class CloudModel(pydantic.BaseModel):
        cloud_description: str
        cloud_name: str
        geo_latitude: float
        geo_longitude: float
        geo_region: str

    clouds: List[CloudModel]


class ProviderEnum(str, Enum):
    aws = 'aws'
    digital_ocean = 'do'
    azure = 'azure'
    google = 'google'
    upcloud = 'upcloud'


class CloudProviderResponse(pydantic.BaseModel):
    class CloudProvider(pydantic.BaseModel):
        code: str
        name: str

    providers: List[CloudProvider]


class RegionEnum(str, Enum):
    africa = 'africa'
    australia = 'australia'
    east_asia = 'east asia'
    europe = 'europe'
    middle_east = 'middle east'
    north_america = 'north america'
    south_america = 'south america'
    south_asia = 'south asia'
    southeast_asia = 'southeast asia'


class SupportRegionResponse(pydantic.BaseModel):
    supported_regions: List[RegionEnum]


class GetCloudsInput(pydantic.BaseModel):
    latitude: Optional[float] = pydantic.Field(ge=-90, le=90)
    longitude: Optional[float] = pydantic.Field(ge=-180, le=180)
    provider: Optional[ProviderEnum]
    region: Optional[RegionEnum]

    @pydantic.root_validator()
    def long_lat_coexist(cls, values: Dict[str, Any]):
        print(values)
        if values.get("latitude") is not None\
                and values.get("longitude") is None:
            raise ValueError("Both latitude and longitude must exist")

        elif values.get("longitude") is not None\
                and values.get("latitude") is None:
            raise ValueError("Both latitude and longitude must exist")

        return values
