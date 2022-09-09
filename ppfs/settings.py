from pydantic import BaseSettings, constr


class Settings(BaseSettings):
    jwt_key: constr(min_length=32)
    mongodb_host: str
    mongodb_username: str
    mongodb_password: str
    default_superuser_name: str
    default_superuser_password: str

    class Config:
        env_file = ".env"     # Use .env file for local development
        env_prefix = "PPFS_"


settings = Settings()
