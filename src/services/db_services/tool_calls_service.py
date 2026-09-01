from ..base_service import Base
from sqlalchemy.ext.asyncio import AsyncSession
from models.tool_call import ToolCall
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
import enum


def _make_json_serializable(obj):
    """Recursively convert non-JSON-serializable types to serializable ones."""
    # UUIDs -> str, Enums -> value or name, tuples/sets -> lists
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, enum.Enum):
        return obj.value if hasattr(obj, "value") else str(obj)
    if isinstance(obj, dict):
        return {k: _make_json_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_make_json_serializable(v) for v in obj]
    return obj

class ToolDBService(Base):
    def __init__(self,db:AsyncSession):
        super().__init__()
        self.db=db

    async def save_tool_calls(self,run_id:UUID,input:dict,tool:str,output:dict):
        self.logger.info("start saving tool call info")

        try:
            # Ensure JSON columns contain only JSON-serializable values
            serializable_input = _make_json_serializable(input)
            serializable_output = _make_json_serializable(output)

            tool_call = ToolCall(run_id=run_id, tool=tool, input=serializable_input, output=serializable_output)
            self.db.add(tool_call)
            await self.db.commit()
            # refresh the instance we just added
            await self.db.refresh(tool_call)
            self.logger.info("Finish Updating tool call info")
            return tool_call
        except SQLAlchemyError:
            self.logger.error("error while saving tool call info",exc_info=True)
            raise
