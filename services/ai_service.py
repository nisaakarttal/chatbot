"""import os
from dotenv import load_dotenv

load_dotenv()

class AIService:

    def __init__(self):
        self.context = self.load_docs()

        # Basit intent bazlı cevap sistemi
        self.flows = {
            "merhaba": "Merhaba 👋 Size nasıl yardımcı olabilirim?",
            "selam": "Selam! 😊 Sana nasıl yardımcı olabilirim?",
            "siparis": "Sipariş durumunu öğrenmek için sipariş numaranı yazabilir misin?",
            "kargo": "Kargo bilgisi için takip numaranı paylaşır mısın?",
            "iade": "İade işlemleri için ürün bilgisi gerekli. Hangi ürünü iade etmek istiyorsun?",
            "tesekkur": "Rica ederim 😊 Başka bir sorunuz var mı?"
        }

    def load_docs(self):
        docs_path = "chatbot/docs"
        content = ""

        if os.path.exists(docs_path):
            for file in os.listdir(docs_path):
                if file.endswith(".txt"):
                    with open(
                        os.path.join(docs_path, file),
                        "r",
                        encoding="utf-8"
                    ) as f:
                        content += f.read() + "\n"

        return content.lower()

    def find_intent(self, question):

        question = question.lower()

        # basit keyword matching
        for key in self.flows:
            if key in question:
                return key

        return None

    def ask(self, question):

        try:
            intent = self.find_intent(question)

            if intent:
                return self.flows[intent]

            # Doküman içinde arama (RAG-like basit sistem)
            if self.context:
                for line in self.context.split("\n"):
                    if question.lower() in line.lower():
                        return line

            return "Bunu tam anlayamadım 😕 Daha açık yazar mısın?"

        except Exception as e:
            print("FLOW ERROR:", e)
            return "Sistem şu anda çalışmıyor."

ai_service = AIService()"""