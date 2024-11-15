from pydantic import BaseModel


class CommonInput(BaseModel):
    pass


class CommonOutput(BaseModel):
    model_config = {'from_attributes': True}
