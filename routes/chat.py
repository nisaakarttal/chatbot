from fastapi import APIRouter
from pydantic import BaseModel
from services.ai_service import ai_service

"""chat.py, frontend’den gelen mesajı alır ve AIService’e göndererek cevabı kullanıcıya döndüren API katmanıdır."""

router = APIRouter(prefix="/api")
"""API router oluşturur"""

class Message(BaseModel):
    user_id: str
    message: str
"""Frontend’den gelen veriyi standardize eder:
kim yazdı (user_id)
ne yazdı (message)"""


"""Chat endpoint’i, kullanıcı mesajı buraya gelir"""
@router.post("/chat")
def chat(msg: Message):

    result = ai_service.ask(msg.message) #mesaj AI service’e gönderilir cevap üretilir
    return result
