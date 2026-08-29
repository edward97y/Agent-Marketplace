from ..base_service import Base
from models.schemas.agent_routes_schema import (CreateAgent,
                                          GetAgent,GetAllAgent,
                                          DeleteAgent,DeleteAllAgent)
from sqlalchemy.ext.asyncio import AsyncSession
from models.agent import Agent
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select,delete

class AgentService(Base):

    def __init__(self,db:AsyncSession):
        super().__init__()
        self.db=db

    async def create_agent(self,data:CreateAgent)->Agent:
        self.logger.info("Starting agent creation")
        agent=Agent(company_id=data.company_id,name=data.name
                    ,description=data.description,
                    type=data.type,is_active=data.is_active)
        try:
            self.db.add(agent)
            await self.db.commit()
            await self.db.refresh(agent)
            self.logger.info("Agent persisted to database successfully")
            return agent

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("Failed to create agent due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to create agent", exc_info=True)
            raise

    async def get_agent_info_by_id(self,info:GetAgent)->Agent| None:
            self.logger.info("Retrieving agent information")
            
            try:

               stmt=select(Agent).where(Agent.id==info.agent_id,
                                        Agent.company_id==info.company_id)

               result=await self.db.execute(stmt)
               return result.scalar_one_or_none()
            
            except SQLAlchemyError:
                self.logger.error("Failed to retrieve agent information due to a database error", exc_info=True)
                raise

            except Exception:
                self.logger.error("Failed to retrieve agent information", exc_info=True)
                raise

    async def get_all_agent_info_by_company_id(self,info:GetAllAgent)->list[Agent]:
                self.logger.info("Retrieving all agents for company")
                
                try:
    
                   stmt=select(Agent).where(Agent.company_id==info.company_id)
    
                   result=await self.db.execute(stmt)
                   return result.scalars().all()
                
                except SQLAlchemyError:
                    self.logger.error("Failed to retrieve company agents due to a database error", exc_info=True)
                    raise

                except Exception:
                    self.logger.error("Failed to retrieve company agents", exc_info=True)
                    raise


    async def delete_agent_by_id(self,info:DeleteAgent):
                    self.logger.info("Deleting agent by ID")
                    
                    try:
        
                       stmt=delete(Agent).where(Agent.company_id==info.company_id,
                                                Agent.id==info.agent_id)
        
                       result=await self.db.execute(stmt)
                       if result.rowcount == 0:
                            return False

                       await self.db.commit()
                       return True
                    
                    except SQLAlchemyError:
                        await self.db.rollback()
                        self.logger.error("Failed to delete agent due to a database error", exc_info=True)
                        raise

                    except Exception:
                        self.logger.error("Failed to delete agent", exc_info=True)
                        raise
    
    async def delete_all_agent_by_company_id(self,info:DeleteAllAgent):
                    self.logger.info("Deleting all agents for company")
                    
                    try:
        
                       stmt=delete(Agent).where(Agent.company_id==info.company_id)
        
                       result=await self.db.execute(stmt)
                       deleted_count = result.rowcount or 0
                       if result.rowcount == 0:
                            return False

                       await self.db.commit()
                       self.logger.info(f"Deleted {deleted_count} agents successfully")
                       return deleted_count

                    except SQLAlchemyError:
                        await self.db.rollback()
                        self.logger.error("Failed to delete company agents due to a database error", exc_info=True)
                        raise

                    except Exception:
                        self.logger.error("Failed to delete company agents", exc_info=True)
                        raise
         