import logging
import yaml
from pydantic import BaseSettings, BaseModel, constr


def read_yaml(filename: str):
    with open(filename, "rb") as file:
        return yaml.safe_load(file)


config: dict = read_yaml("./config/ppfs.yaml")
logging.getLogger("gunicorn.error").info(f"{config=}")


class MongoDBConfig(BaseModel):
    host: str
    username: str
    password: str


class UserConfig(BaseModel):
    username: str
    password: str
    is_admin: bool


class Settings(BaseSettings):
    jwt_key: constr(min_length=32) = config.get("jwt_key")
    mongodb: MongoDBConfig = MongoDBConfig.parse_obj(config.get("mongodb"))
    users: list[UserConfig] = [
        UserConfig.parse_obj(user) for user in config.get("users")
    ]


settings = Settings()
logging.getLogger("gunicorn.error").info(f"{settings.mongodb.host=}")
