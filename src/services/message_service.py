from .base_service import Base
from models.schemas.messages_routes_schema import (GetMessages,SendMessages,MessageResponse)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from .db_services.messages import MessageDBService
from uuid import UUID

from models.enums.db_enum import DatabaseType
from models.enums.db_enum import MessageRole
from .db_services.conversation_service import ConversationService
from models.schemas.conversation_routes_schema import GetConversation
from models.schemas.agent_routes_schema import GetAgent
from .db_services.agent_service import AgentService
from .agent_factory_service import AgentFactory
from .query_service import QueryService
from agent.context import AgentContext
from urllib.parse import quote_plus
from models.company_db_config import CompanyDBConfig
from .db_services.company_db_config_service import CompanyDBService
from models.schemas.company_db_config_routes_schema import GetCompanyDBConfig
from .agent_service import AgentServiceManger
from .company_db_maker_service import CompanyDBService as companydbservice
class MessageService(Base):
    def __init__(self,db:AsyncSession,conversation_id:UUID,agents:dict):
        super().__init__()
        self.db=db
        self.conversation_id=conversation_id
        self.agents=agents
        


    
    async def build_database_url(self,config:CompanyDBConfig):
        
        try:
            self.logger.info("Building company database URL")
            if config.type == DatabaseType.POSTGRES:
                return (
                    f"postgresql+asyncpg://"
                    f"{quote_plus(config.username)}:"
                    f"{quote_plus(config.password)}@"
                    f"{config.host}:{config.port}/"
                    f"{config.name}"
                )

            raise ValueError(f"Unsupported database type: {config.type}")

        except Exception:
            self.logger.error(
                f"Failed to build database URL (db_type={getattr(config, 'type', None)})",
                exc_info=True,
            )
            raise



    async def send_message(self, content:SendMessages):
        self.logger.info("Processing message send request")
        try:
            message_service=MessageDBService(db=self.db)
            save_user_message = await message_service.save_user_message(content=content,conversation_id=self.conversation_id)
            self.logger.info("Saved user message")

            conversation = ConversationService(db=self.db)
            conversation_info = await conversation.get_conversation_info_by_id(
                info=GetConversation(conversation_id=self.conversation_id)
            )
            self.logger.info("Retrieved conversation info")

            agent_service = AgentService(db=self.db)
            agent_info = await agent_service.get_agent_info_by_id(
                GetAgent(company_id=conversation_info.company_id, agent_id=conversation_info.agent_id)
            )
            self.logger.info("Retrieved agent info")

            factory = AgentFactory()
            agent = factory.get_agent(agents=self.agents, agent_type=agent_info.type)

            company_db_service = CompanyDBService(db=self.db)
            company_config = await company_db_service.get_company_by_id(
                info=GetCompanyDBConfig(company_id=conversation_info.company_id)
            )
            company_db_url = await self.build_database_url(config=company_config)
            self.logger.info("Prepared company database connection")

            query_service = QueryService(db=self.db,company_db_service=companydbservice(), company_database_url=company_db_url)
            context = AgentContext(query_service=query_service)

            agent_service_manger = AgentServiceManger(agent=agent,db=self.db)

            messages=await self.to_langchain_messages(
                messages=[save_user_message]
            )
            response,message_id = await agent_service_manger.run_agent(
                messages, conversation_id=self.conversation_id, context=context, company_id=conversation_info.company_id,agent_id=agent_info.id
            )

            result=MessageResponse(conversation_id=self.conversation_id,id=message_id,role=MessageRole.ASSISTANT,content=response)
            self.logger.info("Agent run completed")
            return result

        except SQLAlchemyError:
            self.logger.error(
                f"Database error processing send_message (conversation_id={self.conversation_id})",
                exc_info=True,
            )
            raise

        except Exception:
            self.logger.error(
                f"Unexpected error processing send_message (conversation_id={self.conversation_id})",
                exc_info=True,
            )
            raise
    
