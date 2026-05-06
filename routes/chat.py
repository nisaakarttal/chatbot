from fastapi import APIRouter
from pydantic import BaseModel
# 'chatbot.' takısını buradan da kaldırın
from services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response = await ai_service.generate_response(request.message)
    return {"reply": response}