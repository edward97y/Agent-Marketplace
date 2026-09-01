from .base_service import Base
from uuid import UUID
from models.enums.db_enum import MessageRole
from models.message import Message
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from .db_services.agent_runs_service import AgentRunService
from models.enums.db_enum import RunStatus
class AgentServiceManger(Base):
    def __init__(self,agent,db:AsyncSession):
      super().__init__()
      self.agent=agent
      self.db=db
    async def extract_text(self,content) -> str:
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            return "".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict) and item.get("type") == "text"
            )

        return str(content)
    
    async def save_agent_message(self,content:str,conversation_id:UUID):
        self.logger.info("Saving user message")
        message=Message(conversation_id=conversation_id,content=content,
                        role=MessageRole.ASSISTANT)
        try:
            self.db.add(message)
            await self.db.commit()
            await self.db.refresh(message)
            self.logger.info("User message persisted to database")
            return message
        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error(
                f"Database error saving user message )",
                exc_info=True,
            )
            raise

        except Exception:
            self.logger.error(
                f"Unexpected error saving user message ()",
                exc_info=True,
            )
            raise

    
    
    async def run_agent(self,messages,conversation_id:UUID,
                        context,company_id:UUID,agent_id:UUID):
        
        self.logger.info("start run agent function")
        agent_service=AgentRunService(db=self.db)
        try:
            agent_runs=await agent_service.save_agent_runs_by_conversation_id(conversation_id=conversation_id,
                                                                          agent_id=agent_id,
                                                                          status=RunStatus.RUNNING)
            result=await self.agent.ainvoke( {
            "messages": messages,
            "company_id":company_id,
            "agent_runs_id":agent_runs.id
            },
            context=context,
            config={
                "configurable": {
                    "thread_id": str(conversation_id),

                }
            })
            self.logger.info("saving agent response")
            message = result["messages"][-1]

            content = await self.extract_text(message.content)

            message=await self.save_agent_message(
                conversation_id=conversation_id,
                content=content
            )
            self.logger.info("finish run agent function")
            agent_runs_updated=await agent_service.update_agent_runs_by_conversation_id(agent_runs=agent_runs,status=RunStatus.COMPLETED)
            return content,message.id
        except Exception:
            self.logger.error("error while running the agent",exc_info=True)
            agent_runs_updated=agent_service.update_agent_runs_by_conversation_id(agent_runs=agent_runs,status=RunStatus.FAILED)
                        
            raise