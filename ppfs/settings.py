from pydantic import BaseSettings, constr

from ppfs.models.schemas import UserAuthentication


class Settings(BaseSettings):
    jwt_key: constr(min_length=32)
    mongodb_host: str
    mongodb_username: str
    mongodb_password: str
    allow_register: bool
    default_admin_username: str
    default_admin_password: str
    default_user_username: str
    default_user_password: str

    @property
    def admin_credentials(self) -> UserAuthentication:
        return UserAuthentication(
            username=self.default_admin_username,
            password=self.default_admin_password
        )

    @property
    def user_credentials(self) -> UserAuthentication:
        return UserAuthentication(
            username=self.default_user_username,
            password=self.default_user_password
        )

    class Config:
        env_file = ".env"     # Use .env file for local development
        env_prefix = "PPFS_"


settings = Settings()
