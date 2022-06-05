from pydantic import BaseSettings, constr


class Settings(BaseSettings):
    jwt_key: constr(min_length=32)
    mongodb_host: str
    mongodb_username: str
    mongodb_password: str
    allow_register: bool

    class Config:
        env_file = ".env"
        env_prefix = "PPFS_"


settings = Settings()
