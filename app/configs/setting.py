"""Manages the environment variables using pydantic."""

from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    """Setting Configuration."""

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_REGION: str
    DB_URL: str

    class Config:
        env_file = '.env'
        case_sensitive = False


setting = Setting()  # type: ignore
