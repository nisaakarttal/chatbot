from fastapi import APIRouter
from pydantic import BaseModel
from services.ai_service import ask_ai

router = APIRouter()

class Message(BaseModel):
    message: str

@router.post("/chat")
def chat(msg: Message):
    response = ask_ai(msg.message)
    return {"response": response}