from .base_service import Base
from models.schemas.messages_routes_schema import (GetMessages,SendMessages,MessageResponse)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from models.message import Message
from sqlalchemy import select
from uuid import UUID
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage
)
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
class MessageService(Base):
    def __init__(self,db:AsyncSession,conversation_id:UUID,agents:dict):
        super().__init__()
        self.db=db
        self.conversation_id=conversation_id
        self.agents=agents
        
    async def save_user_message(self,content:str):
        self.logger.info("Saving user message")
        message=Message(conversation_id=self.conversation_id,content=content,
                        role=MessageRole.USER)
        try:
            self.db.add(message)
            await self.db.commit()
            await self.db.refresh(message)
            self.logger.info("User message persisted to database")
            return message
        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error(
                f"Database error saving user message (conversation_id={self.conversation_id})",
                exc_info=True,
            )
            raise

        except Exception:
            self.logger.error(
                f"Unexpected error saving user message (conversation_id={self.conversation_id})",
                exc_info=True,
            )
            raise


    
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


    async def get_messages(self, info: GetMessages)->MessageResponse:
        self.logger.info("Retrieving messages for conversation")
        try:
            stmt = select(Message).where(Message.conversation_id == info.conversation_id)
            result = await self.db.execute(stmt)
            messages = result.scalars().all()
            self.logger.info(f"Retrieved {len(messages)} messages")
            return messages

        except SQLAlchemyError:
            self.logger.error(
                f"Database error retrieving messages (conversation_id={info.conversation_id})",
                exc_info=True,
            )
            raise

        except Exception:
            self.logger.error(
                f"Unexpected error retrieving messages (conversation_id={info.conversation_id})",
                exc_info=True,
            )
            raise


    async def to_langchain_messages(self,
    messages: list[MessageResponse]
    ):
        self.logger.info(f"Converting {len(messages)} messages to LangChain format")
        try:
            result = []

            for message in messages:

                if message.role == "user":
                    result.append(HumanMessage(content=message.content))

                elif message.role == "assistant":
                    result.append(AIMessage(content=message.content))

                elif message.role == "tool":
                    result.append(ToolMessage(content=message.content))

            self.logger.info("Conversion to LangChain format completed")
            return result

        except Exception:
            self.logger.error(
                "Failed to convert messages to LangChain format",
                exc_info=True,
            )
            raise
    
    async def send_message(self, content:SendMessages):
        self.logger.info("Processing message send request")
        try:
            save_user_message = await self.save_user_message(content=content)
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

            query_service = QueryService(db=self.settings.DATABASE_URL, company_db=company_db_url)
            context = AgentContext(query_service=query_service)

            agent_service_manger = AgentServiceManger(agent=agent,db=self.db)
            get_message_info = await self.get_messages(info=GetMessages(conversation_id=self.conversation_id))
            messages = await self.to_langchain_messages(messages=get_message_info)

            response,message_id = await agent_service_manger.run_agent(
                messages, conversation_id=self.conversation_id, context=context, company_id=conversation_info.company_id
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
