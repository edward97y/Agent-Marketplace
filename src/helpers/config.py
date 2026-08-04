from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    EMBEDDING_SIZE:int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

def get_settings() -> Settings:
    return Settings()