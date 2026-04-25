from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+psycopg://postgres:12345@localhost:5432/careerthon_db"
    jwt_secret_key: str = "change_this_secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    upload_dir: str = "uploads"


settings = Settings()
