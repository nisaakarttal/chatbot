import json
import os
from fastapi import APIRouter

"""order.py, sipariş verilerini JSON dosyasından okuyup kullanıcıya API üzerinden sipariş durumunu döndüren basit bir veri servisidir."""

router = APIRouter(prefix="/api")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   #Veri dosyasını tanımlar
DATA_PATH = os.path.join(BASE_DIR, "frontend", "data", "siparisler.json")


@router.get("/order-status/{order_id}")           #Sipariş sorgulama endpoint’i
def order_status(order_id: str):

    if not os.path.exists(DATA_PATH):
        return {"status": "Veri dosyası bulunamadı"}

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        orders = json.load(f)

    order = next(
        (o for o in orders if str(o["order_id"]) == order_id),
        None
    )

    if order:
        return order

    return {"status": "Sipariş bulunamadı"}