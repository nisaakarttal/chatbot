import json
import os
import re


class UserState:
    def __init__(self):
        self.step = "idle"
        self.data = {}


class DialogFlow:
    def __init__(self):
        self.user_states = {}

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "frontend", "data")

        self.products = self.load_json(os.path.join(data_dir, "products.json"))
        self.orders = self.load_json(os.path.join(data_dir, "siparisler.json"))

    def load_json(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def get_state(self, user_id):
        if user_id not in self.user_states:
            self.user_states[user_id] = UserState()

        return self.user_states[user_id]

    def reset_state(self, user_id):
        self.user_states[user_id] = UserState()

    def search_products(self, message):
        message_lower = message.lower()
        found = []

        for product in self.products:
            name = product.get("name", "").lower()

            if any(word in name for word in message_lower.split()):
                found.append(product)

        return found

    def handle_message(self, user_id, message):
        state = self.get_state(user_id)
        message_lower = message.lower()

        # ÜRÜN
        if "ürün" in message_lower:
            return {
                "response": "İşte ürünler:",
                "products": self.products
            }

        found = self.search_products(message)

        if found:
            return {
                "response": "Bulduğum ürünler:",
                "products": found
            }

        # SİPARİŞ
        if "sipariş" in message_lower or "kargo" in message_lower:
            state.step = "waiting_order_id"
            return {
                "response": "Lütfen sipariş numaranızı giriniz."
            }

        if state.step == "waiting_order_id":
            order_id = re.sub(r"\D", "", message)

            for order in self.orders:
                if str(order.get("order_id")) == order_id:
                    self.reset_state(user_id)

                    return {
                        "response":
                            f"📦 Sipariş Durumu: {order.get('status')}\n"
                            f"📅 Teslimat: {order.get('delivery')}"
                    }

            self.reset_state(user_id)

            return {
                "response": "Sipariş bulunamadı."
            }

        # İADE
        if "iade" in message_lower:
            state.step = "waiting_return_order_id"

            return {
                "response": "İade için sipariş numaranızı giriniz."
            }

        if state.step == "waiting_return_order_id":
            order_id = re.sub(r"\D", "", message)

            for order in self.orders:
                if str(order.get("order_id")) == order_id:
                    self.reset_state(user_id)

                    return {
                        "response":
                            f"{order_id} numaralı sipariş için iade talebiniz oluşturuldu."
                    }

            self.reset_state(user_id)

            return {
                "response": "Sipariş bulunamadı."
            }

        return {
            "response":
                "Size yardımcı olabileceğim konular:\n"
                "- Ürün arama\n"
                "- Sipariş takibi\n"
                "- İade işlemleri"
        }


dialog_flow = DialogFlow()