from ..base_service import Base
from sqlalchemy.ext.asyncio import AsyncSession
from models.agent_run import AgentRun
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from models.enums.db_enum import RunStatus
class AgentRunService(Base):
    def __init__(self,db:AsyncSession):
        super().__init__()
        self.db=db

    async def save_agent_runs_by_conversation_id(self,conversation_id:UUID,agent_id:UUID,status:RunStatus):
        self.logger.info("start saving agent runs info")

        try:
            agent=AgentRun(conversation_id=conversation_id,agent_id=agent_id,status=status)
            self.db.add(agent)
            await self.db.flush()
            await self.db.commit()
            self.logger.info("Finish Updating agent runs info")
            return agent
        except SQLAlchemyError:
            self.logger.error("error while saving agent runs info",exc_info=True)
            raise

    async def update_agent_runs_by_conversation_id(self,agent_runs,status:RunStatus):
            self.logger.info("start updating agent runs info")
    
            try:
                agent_runs.status=status
                await self.db.commit()
                self.logger.info("Finish Updating agent runs info")
                return agent_runs
            except SQLAlchemyError:
                self.logger.error("error while updating agent runs info",exc_info=True)
                raise