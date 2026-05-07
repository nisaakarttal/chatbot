from fastapi import APIRouter
from pydantic import BaseModel

from services.dialog_flow import dialog_flow

router = APIRouter(prefix="/api")


class Message(BaseModel):
    user_id: str
    message: str


@router.post("/chat")
def chat(msg: Message):
    result = dialog_flow.handle_message(
        msg.user_id,
        msg.message
    )

    return result