from ..base_service import Base
from sqlalchemy.ext.asyncio import AsyncSession
from models.tool_call import ToolCall
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

class ToolDBService(Base):
    def __init__(self,db:AsyncSession):
        super().__init__()
        self.db=db

    async def save_tool_calls(self,run_id:UUID,input:dict,tool:str,output:dict):
        self.logger.info("start saving tool call info")

        try:
            tool=ToolCall(run_id=run_id,tool=tool,input=input,output=output)
            self.db.add(tool)
            await self.db.commit()
            await self.db.refresh(tool)
            self.logger.info("Finish Updating tool call info")
            return tool
        except SQLAlchemyError:
            self.logger.error("error while saving tool call info",exc_info=True)
            raise
