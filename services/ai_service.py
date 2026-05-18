import json
import os
import re
import unicodedata


class AIService:

    def __init__(self):

        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self.orders_path = os.path.join(BASE_DIR, "frontend", "data", "siparisler.json")
        self.returns_path = os.path.join(BASE_DIR, "frontend", "data", "iadeler.json")
        self.user_state = {}
    """ SS-1 (class + state kısmı) şunu yapıyor:
    Chatbot’un “beyni”ni oluşturuyor (AIService class) user_state ile kullanıcıyı takip ediyor (hafıza gibi)
    Kullanıcı ne sordu, hangi aşamada kaldı → hepsini hatırlayan sistem burası
    Örnek:
    “iade” dedi → sistem bunu kaydediyor, sonra sipariş no istiyor → onu bekliyor, kullanıcı yazınca kaldığı yerden devam
    Chatbot’un konuşmayı hatırlamasını sağlayan kısım"""

    # -------------------------
    # LOADERS
    # -------------------------

    def load_orders(self):
        with open(self.orders_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_returns(self):
        with open(self.returns_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # -------------------------
    # NORMALIZER (FIX)
    # -------------------------

    def normalize(self, text: str) -> str:
        return unicodedata.normalize("NFKD", text)\
            .encode("ascii", "ignore")\
            .decode()\
            .lower()\
            .strip()
    """“Türkçe karakterleri temizliyor, AI karar mekanizmasını sadeleştiriyor”"""

    # -------------------------
    # MAIN ENGINE
    # -------------------------

    """"ask() fonksiyonu: chatbot’un tüm karar verdiği ana yer Kısaca:
       Kullanıcının mesajını alır ve ne cevap verileceğine karar verir."""

    def ask(self, question: str):
        user_id = "global_user"
        state = self.user_state.get(user_id)
        q_raw = question
        q = self.normalize(question)
        print("USER INPUT:", q_raw)
        print("NORMALIZED:", q)

        # =====================================================
        # 1. RETURN STATE
        # =====================================================
        if state == "awaiting_return_id":

            match = re.search(r"\d+", q)

            if not match:
                return {"reply": "Lütfen sipariş numarası yaz (örn: 123)"}

            order_id = match.group()

            returns = self.load_returns()

            r = next(
                (x for x in returns if str(x["order_id"]) == order_id),
                None
            )

            self.user_state[user_id] = None

            if r:
                return {
                    "reply": (
                        f"🔄 İade Durumu\n"
                        f"İade No: {r['return_id']}\n"
                        f"Durum: {r['status']}\n"
                        f"Tarih: {r['created_at']}"
                    )
                }

            return {"reply": "Bu sipariş için iade bulunamadı ❌"}

        # =====================================================
        # 2. ORDER STATE
        # =====================================================
        """“Aynı state machine mantığı sipariş için de var”"""
        if state == "awaiting_order_id":
            match = re.search(r"\d+", q)
            if not match:
                return {"reply": "Lütfen sipariş numarası yaz (örn: 123)"}

            order_id = match.group()

            orders = self.load_orders()

            order = next(
                (o for o in orders if str(o["order_id"]) == order_id),
                None
            )

            self.user_state[user_id] = None

            if order:
                return {
                    "reply": (
                        f"📦 Sipariş Durumu\n"
                        f"ID: {order['order_id']}\n"
                        f"Durum: {order['status']}\n"
                        f"Teslim: {order['delivery']}"
                    )
                }

            return {"reply": "Bu sipariş bulunamadı ❌"}

        # =====================================================
        # 3. İADE BAŞLAT (FIXED NLP)
        # =====================================================
        if any(word in q for word in [
            "iade",
            "return",
            "iade islemi",
            "iade islemi",
            "iade işlemi",
            "iade islemleri"
        ]):

            self.user_state[user_id] = "awaiting_return_id"

            return {
                "reply": "İade için sipariş numaranı yazabilir misin? (örn: 123)"
            }

        # =====================================================
        # 4. SİPARİŞ BAŞLAT
        # =====================================================
        if "siparis" in q or "order" in q:

            self.user_state[user_id] = "awaiting_order_id"

            return {
                "reply": "Sipariş numaranı yazabilir misin? (örn: 123)"
            }

        # =====================================================
        # 5. ÜRÜN ÖNERİSİ
        # =====================================================
        if "urun" in q or "product" in q:

            return {
                "products": [
                    {
                        "name": "Sony WH-1000XM5",
                        "price": 12999,
                        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"
                    },
                    {
                        "name": "Apple Watch Series 9",
                        "price": 18999,
                        "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12"
                    },
                    {
                        "name": "Logitech MX Master 3S",
                        "price": 4999,
                        "image_url": "https://images.unsplash.com/photo-1527814050087-3793815479db"
                    }
                ]
            }

        # =====================================================
        # 6. İNCELE
        # =====================================================
        if "incele" in q:

            name = q.replace("incele", "").strip()

            return {
                "reply": f"🔍 {name} için detay sayfası hazırlanıyor..."
            }

        # =====================================================
        # 7. FALLBACK
        # =====================================================
        return {
            "reply": "Bunu tam anlayamadım 😕 Daha net yazabilir misin?"
        }


ai_service = AIService()