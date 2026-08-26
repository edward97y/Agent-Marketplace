from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    EMBEDDING_SIZE:int

    GEMINI_API_KEY:str
    GEMINI_MODEL_NAME:str


    LANGSMITH_TRACING:bool
    LANGSMITH_API_KEY:str
    LANGSMITH_PROJECT:str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

def get_settings() -> Settings:
    return Settings()