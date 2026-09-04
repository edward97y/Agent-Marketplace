from langchain_core.messages import BaseMessage
from agent.llm import llm
from .base_service import Base

class ConversationSummarizer(Base):

    def __init__(self):
        super().__init__()
        self.llm = llm

    async def summarize(
        self,
        messages: list[BaseMessage],
        previous_summary: str | None = None,
    ) -> str:
        
        conversation = "\n".join(
            f"{message.role}: {message.content}"
            for message in messages
        )

        if previous_summary:
            prompt = f"""
You are a conversation summarizer.

Previous summary:
{previous_summary}

New messages:
{conversation}

Create an updated summary that combines the previous summary
with the new messages.

Keep important information such as:
- Customer requirements
- Products mentioned
- Customer preferences
- Questions and answers
- Important decisions
- Important context needed for future conversation

Do not add information that was not present.

Return only the updated summary.
"""
        else:
            prompt = f"""
You are a conversation summarizer.

Summarize the following conversation:

{conversation}

Keep important information such as:
- Customer requirements
- Products mentioned
- Customer preferences
- Questions and answers
- Important decisions
- Important context needed for future conversation

Do not add information that was not present.

Return only the summary.
"""

        response = await self.llm.ainvoke(prompt)

        self.logger.info("Conversation summarized successfully")
        return response.content[0]["text"]