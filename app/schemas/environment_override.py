from pydantic import BaseModel


class EnvironmentOverrideCreate(BaseModel):
    flag_id: int
    environment_id: int
    value: bool


class EnvironmentOverrideResponse(BaseModel):
    id: int
    flag_id: int
    environment_id: int
    value: bool

    class Config:
        from_attributes = True