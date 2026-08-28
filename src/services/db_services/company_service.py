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
        self.logger.info("start adding company service")
        company=Company(name=data.name,plan=data.plan)
        try:
            self.db.add(company)
            await self.db.commit()
            await self.db.refresh(company)
            self.logger.info("finish adding to data base")
            return company
        
        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("error while creating the company",exc_info=True)
            raise
        
        except Exception:
            self.logger.error("error while creating the company",exc_info=True)
            raise

    async def get_company_by_id(self,info:GetCompany)->Company| None:
            self.logger.info("start get company info service")
            
            try:

               stmt=select(Company).where(Company.id==info.company_id)

               result=await self.db.execute(stmt)
               return result.scalar_one_or_none()
            
            except SQLAlchemyError:
                self.logger.error("error while getting the company info ",exc_info=True)
                raise
            
            except Exception:
                self.logger.error("error while getting the company info ",exc_info=True)
                raise

    async def get_all_company_info(self)->list[Company]:
                self.logger.info("start get all company info service")
                
                try:
    
                   stmt=select(Company)
    
                   result=await self.db.execute(stmt)
                   return result.scalars().all()
                
                except SQLAlchemyError:
                    self.logger.error("error while getting all company info ",exc_info=True)
                    raise
                
                except Exception:
                    self.logger.error("error while getting all company info ",exc_info=True)
                    raise


    async def delete_company_by_id(self,info:DeleteCompany):
                    self.logger.info("start delete company by id service")
                    
                    try:
        
                       stmt=delete(Company).where(Company.id==info.company_id)
        
                       result=await self.db.execute(stmt)
                       if result.rowcount == 0:
                            return False

                       await self.db.commit()
                       return True
                    
                    except SQLAlchemyError:
                        await self.db.rollback()
                        self.logger.error("error while deleting company info ",exc_info=True)
                        raise
                    
                    except Exception:
                        self.logger.error("error while deleting company info ",exc_info=True)
                        raise
    