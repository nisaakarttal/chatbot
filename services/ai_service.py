import os
from openai import OpenAI
from dotenv import load_dotenv
from utils.helper import log

# Çevre değişkenlerini yükle
load_dotenv()

# Client başlatma (api_key parametresini vermeseniz bile
# kütüphane otomatik olarak os.getenv("OPENAI_API_KEY")'e bakar)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Sen bir e-ticaret AI asistanısın.

Görevlerin:
- Ürün öner
- Sipariş sorularına yardımcı ol
- İade sürecini açıkla
- Kullanıcıyı doğru API’ye yönlendir

Kurallar:
- Türkçe konuş
- Kısa ve net ol
- Gereksiz uzatma
- Uydurma bilgi verme
"""


def ask_ai(user_message):
    try:
        # Boş mesaj kontrolü
        if not user_message.strip():
            return "Lütfen bir soru yazın."

        log("USER", user_message)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.5, # Yanıtların tutarlılığını artırır
            max_tokens=250   # Çok uzun ve gereksiz yanıtları sınırlar
        )

        reply = response.choices[0].message.content
        log("AI", reply)
        return reply

    except Exception as e:
        # Hata loglaması yapıp kullanıcıya daha nazik bir mesaj dönmek iyidir
        log("ERROR", str(e))
        return "Şu an teknik bir aksaklık yaşıyorum, lütfen biraz sonra tekrar deneyin."