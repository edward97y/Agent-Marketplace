from .base_service import Base
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from fastapi.encoders import jsonable_encoder
from db.database import async_session
from repository.rag_repo import RagRepository
from models.schemas.rag_schema import RagQuery, RagSearchResult
from models.enums.tool_enum import toolTypes
from .embedding_service import EmbeddingService
from .db_services.tool_calls_service import ToolDBService


class RagService(Base):
    """
    the service behind the `rag_search` tool.
    it opens its own db session (like the tool call logging in QueryService) so it is safe
    when langgraph runs several tools at the same time on the request session.
    """

    def __init__(self, embedding_service: EmbeddingService | None = None):
        super().__init__()
        self.embedding_service = embedding_service or EmbeddingService()

    async def hybrid_search(self, company_id: UUID, agents_runs_id: UUID,
                            query: RagQuery,
                            knowledge_base_id: UUID | None = None) -> list[dict]:
        self.logger.info("Start rag hybrid search")

        try:
            top_k = query.top_k or self.settings.RAG_TOP_K
            query_embedding = await self.embedding_service.embed_query(query.query)

            async with async_session() as db:
                repo = RagRepository(db=db)
                rows = await repo.hybrid_search(
                    company_id=company_id,
                    query_text=query.query,
                    query_embedding=query_embedding,
                    top_k=top_k,
                    candidates_k=max(self.settings.RAG_CANDIDATES_K, top_k),
                    rrf_k=self.settings.RAG_RRF_K,
                    knowledge_base_id=knowledge_base_id,
                )

                output = jsonable_encoder(
                    [RagSearchResult.model_validate(row).model_dump() for row in rows]
                )

                input_data = {
                    "company_id": str(company_id),
                    "agents_runs_id": str(agents_runs_id),
                    "query": query.model_dump(mode="json"),
                }
                await ToolDBService(db=db).save_tool_calls(
                    run_id=agents_runs_id,
                    tool=toolTypes.RAG,
                    input=input_data,
                    output=output,
                )

            self.logger.info(f"Finished rag hybrid search, {len(output)} results")
            return output

        except SQLAlchemyError:
            self.logger.error("SQLAlchemy error while running rag hybrid search", exc_info=True)
            raise
        except Exception:
            self.logger.error("Error while running rag hybrid search", exc_info=True)
            raise
