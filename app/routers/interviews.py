from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import authorize, authorize_interview
from app.types.message_request import MessageRequest
from app.utils.timer import timer
from app.services.chat import ChatService
from app.services.chat_history import ChatHistoryService

# TODO: Remove this import
from app.fakedata import job_desc, resume

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
    dependencies=[
        Depends(authorize),
        Depends(authorize_interview),
    ],
)


@router.post("/{interview_id}/start")
@timer
async def start_conversation(interview_id: str):
    # TODO: Fetch job description and resume

    chat = ChatService(
        interview_id,
        job_description=job_desc,
        resume=resume,
    )

    if chat.is_active():
        raise HTTPException(
            status_code=400,
            detail="Interview already started.",
        )

    chat.set_active()
    return chat.start()


@router.post("/{interview_id}")
@timer
async def conversation(interview_id: str, message: MessageRequest):
    chat = ChatService(
        interview_id,
        job_description=job_desc,
        resume=resume,
    )

    if not chat.is_active():
        raise HTTPException(
            status_code=400,
            detail="Inactive interview.",
        )

    return chat.invoke(message.message)


@router.get("/{interview_id}")
async def get_conversation(interview_id: str):
    messages = ChatHistoryService.get_messages(interview_id)
    if not messages or len(messages) == 0:
        raise HTTPException(
            status_code=404,
            detail="No messages found.",
        )
    messages = messages[1:]  # Remove start message
    return [{"type": message.type, "content": message.content} for message in messages]
