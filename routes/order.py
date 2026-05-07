import json
import os
from fastapi import APIRouter

router = APIRouter()

# JSON dosyasının tam yolunu belirliyoruz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "frontend", "data", "siparisler.json")


@router.get("/order-status/{order_id}")
def order_status(order_id: str):
    try:
        if not os.path.exists(DATA_PATH):
            return {"status": "Veri dosyası bulunamadı"}

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            orders = json.load(f)

        # ID eşleşmesi kontrolü
        order = next((o for o in orders if str(o["order_id"]) == order_id), None)

        if order:
            return order
        return {"status": "Sipariş bulunamadı"}
    except Exception as e:
        return {"status": f"Sunucu hatası: {str(e)}"}