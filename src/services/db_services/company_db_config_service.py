from ..base_service import Base
from sqlalchemy.ext.asyncio import AsyncSession
from models.company_db_config import CompanyDBConfig
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select,delete

from models.schemas.company_db_config_routes_schema import (AddCompanyDBConfig,GetCompanyDBConfig,
                                                            DeleteCompanyDBConfig)

class CompanyDBService(Base):

    def __init__(self,db:AsyncSession):
        super().__init__()
        self.db=db

    async def add_company(self,data:AddCompanyDBConfig)->CompanyDBConfig:
        self.logger.info("Creating company DB config")
        company=CompanyDBConfig(company_id=data.company_id,host=data.host,
                                name=data.name,username=data.username,
                                password=data.password,port=data.port,
                                type=data.type)
        
        try:
            self.db.add(company)
            await self.db.commit()
            await self.db.refresh(company)
            self.logger.info("Persisted company DB config")
            return company

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error(
                f"Database error creating company DB config for company_id={data.company_id}",
                exc_info=True,
            )
            raise

        except Exception:
            self.logger.error(f"Unexpected error creating company DB config for company_id={data.company_id}", exc_info=True)
            raise

    async def get_company_by_id(self,info:GetCompanyDBConfig)->CompanyDBConfig| None:
            self.logger.info("Retrieving company DB config")
            
            try:

               stmt=select(CompanyDBConfig).where(CompanyDBConfig.company_id==info.company_id)

               result=await self.db.execute(stmt)
               return result.scalar_one_or_none()
            
            except SQLAlchemyError:
                self.logger.error(
                    f"Database error retrieving company DB config (company_db_id={info.company_db_id}, company_id={info.company_id})",
                    exc_info=True,
                )
                raise

            except Exception:
                self.logger.error(
                    f"Unexpected error retrieving company DB config (company_db_id={info.company_db_id}, company_id={info.company_id})",
                    exc_info=True,
                )
                raise

    async def delete_company_by_id(self,info:DeleteCompanyDBConfig):
                    self.logger.info("Deleting company DB config")
                    
                    try:
        
                       stmt=delete(CompanyDBConfig).where(CompanyDBConfig.id==info.company_db_id,
                                                          CompanyDBConfig.company_id==info.company_id)
        
                       result=await self.db.execute(stmt)
                       if result.rowcount == 0:
                            return False

                       await self.db.commit()
                       return True
                    
                    except SQLAlchemyError:
                        await self.db.rollback()
                        self.logger.error(
                            f"Database error deleting company DB config (company_db_id={info.company_db_id}, company_id={info.company_id})",
                            exc_info=True,
                        )
                        raise

                    except Exception:
                        self.logger.error(
                            f"Unexpected error deleting company DB config (company_db_id={info.company_db_id}, company_id={info.company_id})",
                            exc_info=True,
                        )
                        raise
    