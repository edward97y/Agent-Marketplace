from .base_service import Base
from uuid import UUID
from models.enums import FilterOperator
from .schema_mapping_service import SchemaMappingService
from sqlalchemy import select,MetaData, Table,func
from sqlalchemy.exc import SQLAlchemyError
from models.schemas.query_schema import Query
from .db_services.tool_calls_service import ToolDBService
from models.enums.tool_enum import toolTypes
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import async_session
from .company_db_maker_service import CompanyDBService
class QueryService(Base):
    def __init__(self,db:AsyncSession,company_db_service:CompanyDBService,company_database_url:str):
        super().__init__()
        self.mapping=SchemaMappingService(db=db)
        self.company_db_service=company_db_service
        self.db=db
        self.company_url=company_database_url

    def _normalize_value(self, value, field_type):
        if field_type == "integer":
            return int(value)

        if field_type == "number":
            return float(value)

        if field_type == "boolean":
            if isinstance(value, bool):
                return value

            if str(value).lower() in {"true", "1", "yes"}:
                return True

            if str(value).lower() in {"false", "0", "no"}:
                return False

            raise ValueError(f"Invalid boolean value: {value}")

        if field_type == "string":
            return str(value)

        return value
    async def search(
        self,
        company_id: UUID,
        agents_runs_id:UUID,
        query:Query
    ):

        self.logger.info("Start query service (search function)")

        
   

        entity_mapping = await self.mapping.get_entity_mapping(
            company_id=company_id,
            entity=query.entity
        )

       
        table_name = entity_mapping["table"]
        fields = entity_mapping["fields"]

        self.logger.info(
            f"Querying table: {table_name}"
        )

        try:
            Sessionlocal=self.company_db_service.get_sessionmaker(company_id=company_id,url=self.company_url)

            async with Sessionlocal()as company_db:
                metadata = MetaData()

                connection = await company_db.connection()

                table = await connection.run_sync(
                    lambda conn: Table(
                        table_name,
                        metadata,
                        autoload_with=conn
                    )
                )



                stmt = select(table)
                if query.filters:
                    for filter_item in query.filters:

                        field = filter_item.field
                        operator = filter_item.operator
                        value = filter_item.value
                        field_mapping = fields.get(field)

                        if not field_mapping:
                            raise ValueError(
                                f"Field '{field}' is not mapped"
                            )

                        column_name = field_mapping["column"]
                        field_type = field_mapping["type"]

                        column = table.c[column_name]

                        value = self._normalize_value(
                                filter_item.value,
                                field_type
                            )

                        if operator == FilterOperator.EQ:

                            if field_type == "string":
                                 stmt = stmt.where(
                                     func.lower(column) == value.lower()
                                 )
                            else:
                                 stmt = stmt.where(
                                     column == value
                                 )
                        elif operator == FilterOperator.CONTAINS:

                            if field_type != "string":
                                raise ValueError(
                                    f"Operator 'contains' can only be used with strings"
                                )

                            stmt = stmt.where(
                                column.ilike(f"%{value}%")
                            )
                        elif operator == FilterOperator.LT:
                            stmt = stmt.where(column < value)

                        elif operator == FilterOperator.GT:
                            stmt = stmt.where(column > value)

                        elif operator == FilterOperator.LTE:
                            stmt = stmt.where(column <= value)

                        elif operator == FilterOperator.GTE:
                            stmt = stmt.where(column >= value)





                result = await company_db.execute(stmt)
                self.logger.info("finish searching function successfully")
                async with async_session() as db:
                    tool_call=ToolDBService(db=db)
                    output=[dict(row) for row in result.mappings().all()]
                    input={"company_id":str(company_id),"agents_runs_id":str(agents_runs_id),"query":query.model_dump(mode="json")}
                
                    _=await tool_call.save_tool_calls(run_id=agents_runs_id,tool=toolTypes.SEARCH,input=input,output=output)
                    return output
        
        except SQLAlchemyError:
            self.logger.error("error while searching db ",exc_info=True)
            raise
        except Exception:
            self.logger.error("error while searching db ",exc_info=True)
            raise