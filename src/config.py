from dotenv import load_dotenv, find_dotenv

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".dev.env"))


class DatabaseSettings(BaseSettings):

    MODE: str

    PROTOCOL: str
    HOST: str
    PORT: str
    NAME: str
    USER: str
    PASSWORD: SecretStr

    model_config = SettingsConfigDict(env_prefix="DB_", extra="ignore")

    @property
    def URL(self):
        return SecretStr(
            f"{self.PROTOCOL}://{self.USER}:{self.PASSWORD.get_secret_value()}@{self.HOST}:{self.PORT}/{self.NAME}"
        )


class JWTSettings(BaseSettings):

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: SecretStr
    ALGORITHM: str

    model_config = SettingsConfigDict(env_prefix="JWT_", extra="ignore")


class SMTPSettings(BaseSettings):

    EMAIL: str
    PASSWORD: SecretStr
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(env_prefix="SMTP_", extra="ignore")


class Settings(BaseSettings):

    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    smtp: SMTPSettings = SMTPSettings()


settings = Settings()
