from .base_repo import Base
from uuid import UUID
from sqlalchemy import select
from models import CompanySchemaMapping
from sqlalchemy.exc import SQLAlchemyError
class SchemaMappingRepository(Base):

    def __init__(self,db):
        super().__init__(db=db)

    async def get_by_company_id(self,company_id:UUID):
        """this function to get the mapping
          from the db using the company id """

        self.logger.info("start the get mapping function ")

        statement=select(CompanySchemaMapping.mapping).where(CompanySchemaMapping.company_id==company_id)
        try:
            result=await self.db.execute(statement)

            self.logger.info("finish the get company mapping function")
            return result.scalar_one_or_none()
        
        except SQLAlchemyError:
            self.logger.error("Error while getting the mapping for the company",exc_info=True)
            raise 
        except Exception:
            self.logger.error("Error while getting the mapping for the company",exc_info=True)
            raise 
        
