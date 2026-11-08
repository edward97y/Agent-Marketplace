from pydantic import BaseModel, Field
from uuid import UUID

class RagQuery(BaseModel):
    """input of the rag tool """

    query:str = Field(
        min_length=1,
        description=(
            "A clear, self-contained search question written in the customer's language. "
            "Rewrite follow-up questions so they make sense without the chat history, "
            "e.g. 'what is the warranty period for BMW cars' instead of 'and for BMW?'."
        )
    )
    top_k:int|None = Field(
        default=None,
        ge=1,
        le=10,
        description="How many passages to return. Leave empty to use the default."
    )

class RagSearchResult(BaseModel):
    """one passage returned by the hybrid search """

    chunk_id:UUID
    document_id:UUID
    filename:str
    content:str
    score:float = Field(description="Reciprocal Rank Fusion score (higher is better)")
    semantic_rank:int|None = Field(default=None, description="Rank in the vector search, null if not found by it")
    keyword_rank:int|None = Field(default=None, description="Rank in the full text search, null if not found by it")
