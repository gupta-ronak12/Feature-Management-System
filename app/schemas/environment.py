from pydantic import BaseModel


class EnvironmentCreate(BaseModel):
    name: str
    description: str | None = None


class EnvironmentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class EnvironmentResponse(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True