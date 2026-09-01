from pydantic import BaseModel
from typing import Any


class FeatureFlagCreate(BaseModel):
    key: str
    name: str
    description: str | None = None
    flag_type: str
    default_value: Any
    enabled: bool = True

class FeatureFlagUpdate(BaseModel):
    key: str | None = None
    name: str | None = None
    description: str | None = None
    flag_type: str | None = None
    default_value: Any | None = None
    enabled: bool | None = None

class FeatureFlagResponse(BaseModel):
    id: int
    key: str
    name: str
    description: str | None
    flag_type: str
    default_value: Any
    enabled: bool

    class Config:
        from_attributes = True