from functools import lru_cache
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from helpers import get_settings
from .base_service import Base


@lru_cache
def get_embedding_client() -> GoogleGenerativeAIEmbeddings:
    """one embedding client for the whole app (same idea as the llm in agent/llm.py)"""
    settings = get_settings()
    return GoogleGenerativeAIEmbeddings(
        model=settings.EMBEDDING_MODEL_NAME,
        google_api_key=settings.GEMINI_API_KEY,
        # must match the pgvector column size (Vector(EMBEDDING_SIZE))
        output_dimensionality=settings.EMBEDDING_SIZE,
    )


class EmbeddingService(Base):
    """
    turn text into vectors.
    gemini embeddings are asymmetric: documents and questions use a different task type,
    this gives better retrieval than embedding both the same way.
    """

    def __init__(self):
        super().__init__()
        self.client = get_embedding_client()

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self.logger.info(f"start embedding {len(texts)} chunks")
        try:
            vectors = await self.client.aembed_documents(texts, task_type="RETRIEVAL_DOCUMENT")
            self.logger.info("finish embedding chunks")
            return vectors
        except Exception:
            self.logger.error("Error while embedding the document chunks", exc_info=True)
            raise

    async def embed_query(self, text: str) -> list[float]:
        self.logger.info("start embedding the query")
        try:
            return await self.client.aembed_query(text, task_type="RETRIEVAL_QUERY")
        except Exception:
            self.logger.error("Error while embedding the query", exc_info=True)
            raise
