from pydantic_settings import BaseSettings


class EnvironmentContainer(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_REGION: str
    DB_URL: str

    class Config:
        env_file = '.env'
        case_sensitive = False


env = EnvironmentContainer()
