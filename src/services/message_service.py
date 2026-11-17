from .base_service import Base
from models.schemas.messages_routes_schema import (GetMessages,SendMessages,MessageResponse)
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from .db_services.messages import MessageDBService
from uuid import UUID

from models.enums.db_enum import DatabaseType
from models.enums.db_enum import MessageRole
from .db_services.conversation_service import ConversationService
from .agent_factory_service import AgentFactory
from .query_service import QueryService
from agent.context import AgentContext
from urllib.parse import quote_plus
from models.company_db_config import CompanyDBConfig
from .agent_service import AgentServiceManger
from .company_db_maker_service import company_db_services
from .schema_mapping_service import SchemaMappingService
from services.actions_service import OrderActionService
from services.rag_service import RagService
class MessageService(Base):
    def __init__(self,db:AsyncSession,conversation_id:UUID,agents:dict,customer_id:UUID|None=None):
        # customer_id is only needed to send a message; reading history doesn't have one
        super().__init__()
        self.db=db
        self.customer_id=customer_id
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



    async def send_message(self, content:SendMessages,background_tasks:BackgroundTasks|None=None):
        self.logger.info("Processing message send request")
        try:
            message_service=MessageDBService(db=self.db)
            await message_service.save_user_message(content=content,conversation_id=self.conversation_id)
            self.logger.info("Saved user message")

            conversation = ConversationService(db=self.db)
            conversation_info,agent_info,company_config = await conversation.get_conversation_context(
                conversation_id=self.conversation_id
            )
            self.logger.info("Retrieved conversation, agent and company DB config")

            factory = AgentFactory()

            agent = factory.get_agent(agents=self.agents, agent_type=agent_info.type)

            company_db_url = await self.build_database_url(config=company_config)
            self.logger.info("Prepared company database connection")

            mapping_service = SchemaMappingService(db=self.db)
            query_service = QueryService(db=self.db,company_db_service=company_db_services,
                                         company_database_url=company_db_url,mapping=mapping_service)
            order_service=OrderActionService(
            db=self.db,
            company_db_service=company_db_services,
            company_database_url=company_db_url,
            mapping=mapping_service,
             )
            context = AgentContext(query_service=query_service, order_action_service=order_service,
                                   rag_service=RagService())

            agent_service_manger = AgentServiceManger(agent=agent,db=self.db)

            response,message_id = await agent_service_manger.run_agent(
                customer_id=self.customer_id, conversation_id=self.conversation_id,
                context=context, company_id=conversation_info.company_id,agent_id=agent_info.id,
                background_tasks=background_tasks
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


    async def get_messages(self, info: GetMessages):
        """conversation history, oldest first"""
        self.logger.info("Retrieving conversation messages")
        message_service = MessageDBService(db=self.db)
        return await message_service.get_messages(info=info)
