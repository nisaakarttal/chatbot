from fastapi import APIRouter
from pydantic import BaseModel
from services.ai_service import ai_service

router = APIRouter(prefix="/api")


class Message(BaseModel):
    user_id: str
    message: str


@router.post("/chat")
def chat(msg: Message):

    result = ai_service.ask(msg.message)

    return result