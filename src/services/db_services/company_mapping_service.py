from ..base_service import Base
from sqlalchemy.ext.asyncio import AsyncSession
from models.company_schema_mapping import CompanySchemaMapping
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select,delete
from models.schemas.company_mapping_schema import (CreateCompanyMapping,
                                                   GetCompanyMapping,
                                                   DeleteCompanyMapping)

class CompanyMappingService(Base):

    def __init__(self,db:AsyncSession):
        super().__init__()
        self.db=db

    async def add_company_mapping(self,data:CreateCompanyMapping)->CompanySchemaMapping:
        self.logger.info("Starting company schema mapping creation")
        company_schema=CompanySchemaMapping(company_id=data.company_id,mapping={
        key: value.model_dump(mode="json")
        for key, value in data.mapping.items()
    })
        try:
            self.db.add(company_schema)
            await self.db.commit()
            await self.db.refresh(company_schema)
            self.logger.info("Company schema mapping persisted to database successfully")
            return company_schema

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("Failed to create company schema mapping due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to create company schema mapping", exc_info=True)
            raise

    async def get_company_mapping_by_id(self,info:GetCompanyMapping)->CompanySchemaMapping| None:
            self.logger.info("Retrieving company schema mapping")
            
            try:

               stmt=select(CompanySchemaMapping).where(CompanySchemaMapping.company_id==info.company_id)

               result=await self.db.execute(stmt)
               return result.scalar_one_or_none()
            
            except SQLAlchemyError:
                self.logger.error("Failed to retrieve company schema mapping due to a database error", exc_info=True)
                raise

            except Exception:
                self.logger.error("Failed to retrieve company schema mapping", exc_info=True)
                raise

    async def delete_company_mapping_by_id(self,info:DeleteCompanyMapping):
                    self.logger.info("Deleting company schema mapping")
                    
                    try:
        
                       stmt=delete(CompanySchemaMapping).where(CompanySchemaMapping.company_id==info.company_id)
        
                       result=await self.db.execute(stmt)
                       if result.rowcount == 0:
                            return False

                       await self.db.commit()
                       return True
                    
                    except SQLAlchemyError:
                        await self.db.rollback()
                        self.logger.error("Failed to delete company schema mapping due to a database error", exc_info=True)
                        raise

                    except Exception:
                        self.logger.error("Failed to delete company schema mapping", exc_info=True)
                        raise
    