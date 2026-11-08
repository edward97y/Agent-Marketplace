import re
from .base_repo import Base
from uuid import UUID
from sqlalchemy import select, func, cast, Text, literal_column
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models import DocumentChunk, Embedding, Document, KnowledgeBase


# the 'simple' text search config keeps every word (so it works for arabic and english),
# which means words like "the" / "في" would match almost every chunk in the OR keyword query.
# we drop them from the question before building the keyword query.
STOP_WORDS = {
    # english
    "a", "an", "the", "and", "or", "but", "if", "of", "to", "in", "on", "at", "by", "for", "with",
    "from", "about", "as", "into", "is", "are", "was", "were", "be", "been", "am", "do", "does",
    "did", "have", "has", "had", "can", "could", "will", "would", "should", "may", "might", "i",
    "me", "my", "we", "our", "you", "your", "he", "she", "it", "its", "they", "them", "their",
    "this", "that", "these", "those", "what", "which", "who", "whom", "when", "where", "why",
    "how", "there", "here", "any", "some", "get", "got", "please", "tell", "know", "want", "not",
    # arabic
    "في", "من", "على", "إلى", "الى", "عن", "مع", "هل", "ما", "ماذا", "متى", "أين", "اين", "كيف",
    "كم", "لماذا", "هو", "هي", "هذا", "هذه", "ذلك", "تلك", "التي", "الذي", "أن", "ان", "إن", "أو",
    "او", "و", "يا", "لو", "لا", "عايز", "عاوز", "ايه", "إيه", "فين", "امتى", "ازاي", "إزاي",
}


def keyword_terms(text: str) -> str:
    """keep the meaningful words of the question for the full text side of the search"""
    words = re.findall(r"\w[\w-]*", text.lower())
    kept = [word for word in words if word not in STOP_WORDS]
    # if the question is only stop words keep it as it is instead of searching for nothing
    return " ".join(kept or words)


class RagRepository(Base):
    """
    all the pgvector / full text sql of the rag lives here.

    hybrid search =
        1. semantic search  : cosine distance between the query embedding and the chunk embeddings (pgvector)
        2. keyword search   : postgres full text search on document_chunks.search_vector (tsvector + GIN)
        3. fusion           : Reciprocal Rank Fusion  score = 1/(k + semantic_rank) + 1/(k + keyword_rank)
    everything runs in ONE sql query (3 CTEs) so there is only one round trip to the db.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db=db)

    async def add_chunks(self, document_id: UUID, chunks: list[str],
                         embeddings: list[list[float]]) -> int:
        """insert the chunks and their embeddings of a document.
           it only flushes, the caller is responsible for the commit (one transaction per document)"""

        self.logger.info(f"start inserting {len(chunks)} chunks")

        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have the same length")

        try:
            rows = [
                DocumentChunk(
                    document_id=document_id,
                    chunk_index=index,
                    content=content,
                    embeddings=[Embedding(embedding=vector)],
                )
                for index, (content, vector) in enumerate(zip(chunks, embeddings))
            ]
            self.db.add_all(rows)
            await self.db.flush()

            self.logger.info("finish inserting chunks")
            return len(rows)

        except SQLAlchemyError:
            self.logger.error("Error while inserting the document chunks", exc_info=True)
            raise

    def _company_scope(self, stmt, company_id: UUID, knowledge_base_id: UUID | None):
        """restrict a chunk query to the company (and optionally one knowledge base)"""

        stmt = (
            stmt.join(Document, Document.id == DocumentChunk.document_id)
                .join(KnowledgeBase, KnowledgeBase.id == Document.knowledge_base_id)
                .where(KnowledgeBase.company_id == company_id)
        )
        if knowledge_base_id is not None:
            stmt = stmt.where(KnowledgeBase.id == knowledge_base_id)
        return stmt

    async def hybrid_search(self, company_id: UUID, query_text: str,
                            query_embedding: list[float], top_k: int,
                            candidates_k: int, rrf_k: int,
                            knowledge_base_id: UUID | None = None) -> list[dict]:
        """run semantic + keyword search and fuse them with RRF"""

        self.logger.info("start hybrid search")

        try:
            # ---------- 1. semantic search (pgvector cosine distance) ----------
            distance = Embedding.embedding.cosine_distance(query_embedding)

            semantic = self._company_scope(
                select(
                    DocumentChunk.id.label("chunk_id"),
                    func.row_number().over(order_by=distance).label("rank"),
                ).join(Embedding, Embedding.chunk_id == DocumentChunk.id),
                company_id, knowledge_base_id,
            ).order_by(distance).limit(candidates_k).cte("semantic")

            # ---------- 2. keyword search (postgres full text) ----------
            # plainto_tsquery ANDs all the words -> too strict for a natural question,
            # so we turn the '&' into '|' (OR) and let ts_rank_cd reward chunks matching more words
            ts_query = func.to_tsquery(
                "simple",
                func.replace(cast(func.plainto_tsquery("simple", keyword_terms(query_text)), Text), "&", "|"),
            )
            text_rank = func.ts_rank_cd(DocumentChunk.search_vector, ts_query)

            keyword = self._company_scope(
                select(
                    DocumentChunk.id.label("chunk_id"),
                    func.row_number().over(order_by=text_rank.desc()).label("rank"),
                ).where(DocumentChunk.search_vector.op("@@")(ts_query)),
                company_id, knowledge_base_id,
            ).order_by(text_rank.desc()).limit(candidates_k).cte("keyword")

            # ---------- 3. Reciprocal Rank Fusion ----------
            one = literal_column("1.0")
            score = (
                func.coalesce(one / (rrf_k + semantic.c.rank), 0.0)
                + func.coalesce(one / (rrf_k + keyword.c.rank), 0.0)
            )

            fused = (
                select(
                    func.coalesce(semantic.c.chunk_id, keyword.c.chunk_id).label("chunk_id"),
                    score.label("score"),
                    semantic.c.rank.label("semantic_rank"),
                    keyword.c.rank.label("keyword_rank"),
                )
                .select_from(
                    semantic.join(keyword, semantic.c.chunk_id == keyword.c.chunk_id, full=True)
                )
                .cte("fused")
            )

            stmt = (
                select(
                    fused.c.chunk_id,
                    DocumentChunk.document_id,
                    Document.filename,
                    DocumentChunk.content,
                    fused.c.score,
                    fused.c.semantic_rank,
                    fused.c.keyword_rank,
                )
                .join(DocumentChunk, DocumentChunk.id == fused.c.chunk_id)
                .join(Document, Document.id == DocumentChunk.document_id)
                .order_by(fused.c.score.desc())
                .limit(top_k)
            )

            result = await self.db.execute(stmt)
            rows = [dict(row) for row in result.mappings().all()]

            self.logger.info(f"finish hybrid search, found {len(rows)} chunks")
            return rows

        except SQLAlchemyError:
            self.logger.error("Error while running the hybrid search", exc_info=True)
            raise
        except Exception:
            self.logger.error("Error while running the hybrid search", exc_info=True)
            raise
