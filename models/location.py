from pydantic import BaseModel, Field


class Location(BaseModel):
    id: str = Field(..., alias="_id")
    city: str = Field(...)
    state: str = Field(...)
    state_code: str = Field(...)
    country_code: str = Field(...)
    postal_code: str = Field(...)
    latitude: str = Field(...)
    longitude: str = Field(...)
    province_code: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "5f4e7d4b0a4e7b8e1b1c9a9d",
                "city": "San Francisco",
                "state": "California",
                "state_code": "CA",
                "country_code": "United States",
                "postal_code": "94102",
                "latitude": "37.781",
                "longitude": "-122.411",
                "province_code": "CA"
            }
        }
