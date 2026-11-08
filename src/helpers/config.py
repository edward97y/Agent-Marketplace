from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    EMBEDDING_SIZE:int
    EMBEDDING_MODEL_NAME:str="gemini-embedding-001"

    GEMINI_API_KEY:str
    GEMINI_MODEL_NAME:str
    GEMINI_MAX_RETRIES:int=1
    GEMINI_TIMEOUT_SECONDS:float=60

  
    LOCAL_LLM_ENABLED:bool=True
    LOCAL_LLM_MODEL_NAME:str="qwen3.5:4b"
    OLLAMA_BASE_URL:str="http://localhost:11434"
    LOCAL_LLM_NUM_CTX:int=16384
    LOCAL_LLM_TIMEOUT_SECONDS:float=300

    RAG_CHUNK_SIZE:int=1000
    RAG_CHUNK_OVERLAP:int=150
    RAG_TOP_K:int=5
    RAG_CANDIDATES_K:int=20
    RAG_RRF_K:int=60
    RAG_MAX_FILE_SIZE_MB:int=10

    LANGSMITH_TRACING:bool
    LANGSMITH_API_KEY:str
    LANGSMITH_PROJECT:str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

def get_settings() -> Settings:
    return Settings()
