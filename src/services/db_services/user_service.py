from ..base_service import Base
from models.schemas.user_routes_schema import (AddUser,GetAllUser
                                               ,GetUser,DeleteUser)
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select,delete
from services.core.security import plan_to_hash_password
class UserService(Base):

    def __init__(self,db:AsyncSession):
        super().__init__()
        self.db=db

    async def create_user(self,data:AddUser)->User:
        self.logger.info("start create user service")

        self.logger.info("start hashing password")
        password=plan_to_hash_password(password=data.password)
        user=User(company_id=data.company_id,role=data.role
                   ,email=data.email,password_hash=password)
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            self.logger.info("finish adding to data base")
            return user
        
        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("error while creating the user",exc_info=True)
            raise
        
        except Exception:
            self.logger.error("error while creating the user",exc_info=True)
            raise

    async def get_user_info_by_id(self,info:GetUser)->User| None:
            self.logger.info("start get user info service")
            
            try:

               stmt=select(User).where(User.id==info.user_id,
                                        User.company_id==info.company_id)

               result=await self.db.execute(stmt)
               return result.scalar_one_or_none()
            
            except SQLAlchemyError:
                self.logger.error("error while getting the user info ",exc_info=True)
                raise
            
            except Exception:
                self.logger.error("error while getting the user info ",exc_info=True)
                raise

    async def get_all_user_info_by_company_id(self,info:GetAllUser)->list[User]:
                self.logger.info("start get all user info service")
                
                try:
    
                   stmt=select(User).where(User.company_id==info.company_id)
    
                   result=await self.db.execute(stmt)
                   return result.scalars().all()
                
                except SQLAlchemyError:
                    self.logger.error("error while getting all company user info ",exc_info=True)
                    raise
                
                except Exception:
                    self.logger.error("error while getting all company user info ",exc_info=True)
                    raise


    async def delete_user_by_id(self,info:DeleteUser):
                    self.logger.info("start delete user by id service")
                    
                    try:
        
                       stmt=delete(User).where(User.company_id==info.company_id,
                                                User.id==info.user_id)
        
                       result=await self.db.execute(stmt)
                       if result.rowcount == 0:
                            return False

                       await self.db.commit()
                       return True
                    
                    except SQLAlchemyError:
                        await self.db.rollback()
                        self.logger.error("error while deleting user info ",exc_info=True)
                        raise
                    
                    except Exception:
                        self.logger.error("error while deleting user info ",exc_info=True)
                        raise
    