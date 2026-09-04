from helpers import get_logger,get_settings
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage
)
from models.schemas.messages_routes_schema import MessageResponse
class Base:
    def __init__(self):
         
        self.logger = get_logger(self.__class__.__name__)
        self.settings=get_settings()

    
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
    