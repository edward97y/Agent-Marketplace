from ..base_service import Base
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from models.conversation import Conversation
from models.agent import Agent
from models.company_db_config import CompanyDBConfig
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select,delete,and_

from models.schemas.conversation_routes_schema import (CreateConversation,GetAgentConversation,
                                               GetConversation,GetUserConversation,
                                               DeleteAgentConversation,DeleteConversation)

class ConversationService(Base):

    def __init__(self,db:AsyncSession):
        super().__init__()
        self.db=db

    async def add_conversation(self,data:CreateConversation)->Conversation:
        self.logger.info("Starting conversation creation")
        conversation=Conversation(company_id=data.company_id,agent_id=data.agent_id,
                                  user_id=data.user_id)
        try:
            self.db.add(conversation)
            await self.db.commit()
            await self.db.refresh(conversation)
            self.logger.info("Conversation persisted to database successfully")
            return conversation

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("Failed to create conversation due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to create conversation", exc_info=True)
            raise

    async def get_agent_conversations(self,info:GetAgentConversation)->Conversation| None:
            self.logger.info("Retrieving agent conversations")
            
            try:

               stmt=select(Conversation).where(Conversation.company_id==info.company_id,
                                               Conversation.agent_id==info.agent_id)

               result=await self.db.execute(stmt)
               return result.scalar_one_or_none()

            except SQLAlchemyError:
                self.logger.error("Failed to retrieve agent conversations due to a database error", exc_info=True)
                raise

            except Exception:
                self.logger.error("Failed to retrieve agent conversations", exc_info=True)
                raise

    async def get_user_conversations(self,info:GetUserConversation)->Conversation| None:
                self.logger.info("Retrieving user conversations")
                
                try:
    
                   stmt=select(Conversation).where(Conversation.company_id==info.company_id,
                                                   Conversation.user_id==info.user_id)

                   result=await self.db.execute(stmt)
                   return result.scalar_one_or_none()

                except SQLAlchemyError:
                    self.logger.error("Failed to retrieve user conversations due to a database error", exc_info=True)
                    raise

                except Exception:
                    self.logger.error("Failed to retrieve user conversations", exc_info=True)
                    raise

    async def get_conversation_info_by_id(self,info:GetConversation)->Conversation:
                    self.logger.info("Retrieving conversation by ID")
                    
                    try:
                    
                        stmt=select(Conversation).where(Conversation.id==info.conversation_id)

                        result=await self.db.execute(stmt)
                        return result.scalar_one_or_none()
                    
                    except SQLAlchemyError:
                        self.logger.error("Failed to retrieve conversation by ID due to a database error", exc_info=True)
                        raise
                    
                    except Exception:
                        self.logger.error("Failed to retrieve conversation by ID", exc_info=True)
                        raise

    async def get_conversation_context(self,conversation_id:UUID)->tuple[Conversation,Agent,CompanyDBConfig]:
                    self.logger.info("Retrieving conversation, agent and company DB config")

                    try:

                        stmt=(
                            select(Conversation,Agent,CompanyDBConfig)
                            .outerjoin(Agent,and_(Agent.id==Conversation.agent_id,
                                                  Agent.company_id==Conversation.company_id))
                            .outerjoin(CompanyDBConfig,CompanyDBConfig.company_id==Conversation.company_id)
                            .where(Conversation.id==conversation_id)
                        )

                        result=await self.db.execute(stmt)
                        row=result.first()

                    except SQLAlchemyError:
                        self.logger.error("Failed to retrieve conversation context due to a database error", exc_info=True)
                        raise

                    if row is None:
                        raise ValueError("Conversation not found")

                    conversation,agent,company_config=row

                    if agent is None:
                        raise ValueError("Agent not found for this conversation")

                    if company_config is None:
                        raise ValueError("Company database config not found")

                    return conversation,agent,company_config

    async def delete_conversation_by_id(self,info:DeleteConversation):
                    self.logger.info("Deleting conversation by ID")
                    
                    try:
        
                       stmt=delete(Conversation).where(Conversation.company_id==info.company_id,Conversation.id==info.conversation_id)

                       result=await self.db.execute(stmt)
                       if result.rowcount == 0:
                            return False

                       await self.db.commit()
                       return True
                    
                    except SQLAlchemyError:
                        await self.db.rollback()
                        self.logger.error("Failed to delete conversation due to a database error", exc_info=True)
                        raise
                    
                    except Exception:
                        self.logger.error("Failed to delete conversation", exc_info=True)
                        raise
    
    async def delete_agent_conversation_by_id(self,info:DeleteAgentConversation):
                    self.logger.info("Deleting agent conversation by ID")
                    
                    try:
        
                       stmt=delete(Conversation).where(Conversation.company_id==info.company_id,Conversation.agent_id==info.agent_id)

                       result=await self.db.execute(stmt)
                       if result.rowcount == 0:
                            return False

                       await self.db.commit()
                       return True
                    
                    except SQLAlchemyError:
                        await self.db.rollback()
                        self.logger.error("Failed to delete agent conversations due to a database error", exc_info=True)
                        raise
                    
                    except Exception:
                        self.logger.error("Failed to delete agent conversations", exc_info=True)
                        raise
    