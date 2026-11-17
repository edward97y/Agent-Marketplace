from uuid import UUID

from sqlalchemy import MetaData, Table
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class CompanyDBServices:
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
        self.urls: dict[UUID, str] = {}
        self.tables: dict[tuple[UUID, str], Table] = {}

    def _forget_company(self, company_id: UUID) -> AsyncEngine | None:
        engine = self.engines.pop(company_id, None)
        self.sessionmakers.pop(company_id, None)
        self.urls.pop(company_id, None)
        for key in [key for key in self.tables if key[0] == company_id]:
            self.tables.pop(key, None)
        return engine

    async def get_sessionmaker(
        self,
        company_id: UUID,
        url: str,
    ) -> async_sessionmaker[AsyncSession]:
        """
        Get or create a session maker for a company.
        """

        old_engine = None

        if self.urls.get(company_id) != url:
            old_engine = self._forget_company(company_id)

            engine = create_async_engine(
                url,
                pool_pre_ping=True,
            )

            self.engines[company_id] = engine
            self.urls[company_id] = url

            self.sessionmakers[company_id] = async_sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

        sessionmaker = self.sessionmakers[company_id]

        if old_engine is not None:
            await old_engine.dispose()

        return sessionmaker

    async def get_table(
        self,
        company_id: UUID,
        table_name: str,
        connection: AsyncConnection,
    ) -> Table:
        key = (company_id, table_name)
        table = self.tables.get(key)

        if table is None:
            table = await connection.run_sync(
                lambda sync_conn: Table(
                    table_name,
                    MetaData(),
                    autoload_with=sync_conn,
                )
            )
            self.tables[key] = table

        return table

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

        engine = self._forget_company(company_id)

        if engine:
            await engine.dispose()

    async def close_all(self) -> None:
        """
        Close all company database engines.
        """

        engines = list(self.engines.values())

        self.engines.clear()
        self.sessionmakers.clear()
        self.urls.clear()
        self.tables.clear()

        for engine in engines:
            await engine.dispose()


company_db_services = CompanyDBServices()
