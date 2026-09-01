from uuid import UUID

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class CompanyDBService:
    """
    Manages database engines and session makers for company databases.

    One Engine/connection pool is maintained per company.
    A new AsyncSession can be created from the cached session maker.
    """

    def __init__(self):
        self.engines: dict[UUID, AsyncEngine] = {}
        self.sessionmakers: dict[
            UUID,
            async_sessionmaker[AsyncSession]
        ] = {}

    def get_sessionmaker(
        self,
        company_id: UUID,
        url: str,
    ) -> async_sessionmaker[AsyncSession]:
        """
        Get or create a session maker for a company.
        """

        if company_id not in self.sessionmakers:

            engine = create_async_engine(
                url,
                pool_pre_ping=True,
            )

            self.engines[company_id] = engine

            self.sessionmakers[company_id] = async_sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

        return self.sessionmakers[company_id]

    def get_engine(
        self,
        company_id: UUID,
    ) -> AsyncEngine | None:
        """
        Get the cached engine for a company.
        """

        return self.engines.get(company_id)

    async def close_company(
        self,
        company_id: UUID,
    ) -> None:
        """
        Close a company's engine and remove it from the cache.
        """

        engine = self.engines.pop(company_id, None)

        self.sessionmakers.pop(company_id, None)

        if engine:
            await engine.dispose()

    async def close_all(self) -> None:
        """
        Close all company database engines.
        """

        for engine in self.engines.values():
            await engine.dispose()

        self.engines.clear()
        self.sessionmakers.clear()