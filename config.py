from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    deta_space_app_hostname: str
    deta_project_key: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_config():
    return Settings()
