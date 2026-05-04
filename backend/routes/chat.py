
from fastapi import APIRouter
from services.ai_service import get_response

router = APIRouter()

@router.post("/chat")
def chat(message: dict):
    return {"reply": get_response(message["message"])}
