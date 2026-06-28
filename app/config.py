from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # JWT & Auth
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Database
    db_user: str
    db_password: str
    db_host: str
    db_name: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()