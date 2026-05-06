class AIService:
    async def generate_response(self, text: str) -> str:
        text = text.lower()
        if "merhaba" in text or "selam" in text:
            return "Merhaba! Size nasıl yardımcı olabilirim?"
        elif "sipariş" in text:
            return "Sipariş durumunuzu kontrol etmemi ister misiniz?"
        elif "ürün" in text:
            return "Hangi ürün hakkında bilgi almak istiyorsunuz?"
        else:
            return "Anladım, bu konuda size yardımcı olmaya çalışacağım."