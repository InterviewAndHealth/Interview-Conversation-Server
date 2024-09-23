from functools import wraps
import time
from fastapi import HTTPException

from app import INTERVIEW_DURATION
from app.services.redis import RedisService
from app.services.chat_history import ChatHistoryService


def _fetch_or_update_start_time(interview_id: str) -> float:
    """Fetch or update the start time of the interview."""
    start_time = RedisService.get_time(interview_id)
    if start_time is None:
        # Store the current time if it's a new interview
        start_time = time.time()
        RedisService.set_time(interview_id, start_time)
    return float(start_time)


def _calculate_elapsed_time(interview_id: str) -> float:
    """Calculate the elapsed time for the interview."""
    start_time = _fetch_or_update_start_time(interview_id)
    return time.time() - start_time


def _is_reaching_end_80percent(elapsed_time: float) -> bool:
    """Check if the interview is in the last 20% of time."""
    session_duration = INTERVIEW_DURATION * 60
    return elapsed_time >= session_duration * 0.8


def _is_reaching_end_90percent(elapsed_time: float) -> bool:
    """Check if the interview is in the last 10% of time."""
    session_duration = INTERVIEW_DURATION * 60
    return elapsed_time >= session_duration * 0.9


def _is_interview_ended(elapsed_time: float) -> bool:
    """Check if the interview is ended."""
    session_duration = INTERVIEW_DURATION * 60
    return elapsed_time >= session_duration


def timer(func):
    """Decorator to check the time of the interview."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        interview_id = kwargs.get("interview_id")
        elapsed_time = _calculate_elapsed_time(interview_id)

        if _is_interview_ended(elapsed_time):
            raise HTTPException(
                status_code=400,
                detail="Interview has ended. Thank you for your time and responses.",
            )

        elif _is_reaching_end_90percent(elapsed_time):
            ChatHistoryService.add_system_message(
                interview_id,
                "Interview is 90 percent complete. This will be the last response from the interviewer. Mention that your feedback will be shared with you soon and thank the candidate for their time.",
            )

        elif _is_reaching_end_80percent(elapsed_time):
            ChatHistoryService.add_system_message(
                interview_id,
                "Interview is 80 percent complete. This will be second to the last question. Ask about the final questions, experiences and wrap up.",
            )

        return await func(*args, **kwargs)

    return wrapper
