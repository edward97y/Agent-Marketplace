import os

DUMMY_ENV = {
    "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test",
    "EMBEDDING_SIZE": "1536",
    "GEMINI_API_KEY": "test-gemini-key",
    "GEMINI_MODEL_NAME": "test-gemini-model",
    "LANGSMITH_TRACING": "false",
    "LANGSMITH_API_KEY": "test-langsmith-key",
    "LANGSMITH_PROJECT": "test-project",
}

for key, value in DUMMY_ENV.items():
    os.environ.setdefault(key, value)
