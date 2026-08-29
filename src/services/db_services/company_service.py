from ..base_service import Base
from sqlalchemy.ext.asyncio import AsyncSession
from models.company import Company
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select,delete

from models.schemas.company_routes_schema import (AddCompany,
                                          GetCompany,DeleteCompany)

class CompanyService(Base):

    def __init__(self,db:AsyncSession):
        super().__init__()
        self.db=db

    async def add_company(self,data:AddCompany)->Company:
        self.logger.info("Starting company creation")
        company=Company(name=data.name,plan=data.plan)
        try:
            self.db.add(company)
            await self.db.commit()
            await self.db.refresh(company)
            self.logger.info("Company persisted to database successfully")
            return company

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("Failed to create company due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to create company", exc_info=True)
            raise

    async def get_company_by_id(self,info:GetCompany)->Company| None:
            self.logger.info("Retrieving company information")
            
            try:

               stmt=select(Company).where(Company.id==info.company_id)

               result=await self.db.execute(stmt)
               return result.scalar_one_or_none()
            
            except SQLAlchemyError:
                self.logger.error("Failed to retrieve company information due to a database error", exc_info=True)
                raise

            except Exception:
                self.logger.error("Failed to retrieve company information", exc_info=True)
                raise

    async def get_all_company_info(self)->list[Company]:
                self.logger.info("Retrieving all companies")
                
                try:
    
                   stmt=select(Company)
    
                   result=await self.db.execute(stmt)
                   return result.scalars().all()
                
                except SQLAlchemyError:
                    self.logger.error("Failed to retrieve companies due to a database error", exc_info=True)
                    raise

                except Exception:
                    self.logger.error("Failed to retrieve companies", exc_info=True)
                    raise


    async def delete_company_by_id(self,info:DeleteCompany):
                    self.logger.info("Deleting company by ID")
                    
                    try:
        
                       stmt=delete(Company).where(Company.id==info.company_id)
        
                       result=await self.db.execute(stmt)
                       if result.rowcount == 0:
                            return False

                       await self.db.commit()
                       return True
                    
                    except SQLAlchemyError:
                        await self.db.rollback()
                        self.logger.error("Failed to delete company due to a database error", exc_info=True)
                        raise

                    except Exception:
                        self.logger.error("Failed to delete company", exc_info=True)
                        raise
    