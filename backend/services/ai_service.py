
def get_response(message: str):
    message = message.lower()

    if "merhaba" in message:
        return "Merhaba 👋"

    if "ürün" in message:
        return "Ürünler data klasöründe"

    if "sipariş" in message:
        return "Siparişler kayıtlı"

    return "Anlayamadım"
