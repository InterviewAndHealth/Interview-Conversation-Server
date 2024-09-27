from fastapi import HTTPException
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.services.chain import ChainService
from app.services.chat_history import ChatHistoryService
from app.services.redis import RedisService
from app.types.message_response import MessageResponse


class ChatService:
    """Service for handling conversation chat."""

    _INPUT_MESSAGES_KEY = "input"
    _HISTORY_MESSAGES_KEY = "history"

    def __init__(
        self,
        interview_id: str,
        job_description: str = None,
        resume: str = None,
    ):
        self.interview_id = interview_id

        self.chain = ChainService(
            job_description=job_description,
            resume=resume,
        ).get_chain()

        self.runnable = RunnableWithMessageHistory(
            self.chain,
            ChatHistoryService.get_history,
            input_messages_key=self._INPUT_MESSAGES_KEY,
            history_messages_key=self._HISTORY_MESSAGES_KEY,
        )

    def set_active(self):
        """Set the chat service to active."""
        RedisService.set_status(self.interview_id, RedisService.Status.ACTIVE)

    def set_inactive(self):
        """Set the chat service to inactive."""
        RedisService.set_status(self.interview_id, RedisService.Status.INACTIVE)

    def is_active(self) -> bool:
        """Check if the chat service is active."""
        return RedisService.get_status(self.interview_id) == RedisService.Status.ACTIVE

    def invoke(self, message: str) -> str:
        """Invoke the chat service with a message."""
        if not self.is_active():
            raise HTTPException(
                status_code=400,
                detail="Inactive interview.",
            )

        response = self.runnable.invoke(
            {self._INPUT_MESSAGES_KEY: message},
            config={
                "configurable": {"session_id": self.interview_id},
            },
        )
        # for i in response['messages']:
        #     print(i.content)
        #     print("*"*100)
        return MessageResponse(message=response['messages'][-1].content)

    def start(self) -> str:
        """Start the chat service."""
        return self.invoke("Hello")
