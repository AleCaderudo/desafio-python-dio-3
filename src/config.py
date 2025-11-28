from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

    database_url: str
    environment: str = "production"

    # JWT settings
    secret_key: str = "change_me"
    access_token_expire_minutes: int = 60
    jwt_algorithm: str = "HS256"

settings = Settings()
