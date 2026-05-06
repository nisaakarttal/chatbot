from fastapi import APIRouter

router = APIRouter()

orders = {
    "1001": "Kargoda",
    "1002": "Hazırlanıyor",
    "1003": "Teslim edildi"
}

@router.get("/order-status/{order_id}")
def order_status(order_id: str):
    return {
        "order_id": order_id,
        "status": orders.get(order_id, "Sipariş bulunamadı")
    }