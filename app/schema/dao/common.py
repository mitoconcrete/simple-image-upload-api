from pydantic import BaseModel, ConfigDict


class CommonInput(BaseModel):
    pass


class CommonOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
