import os
from fastapi import FastAPI
app = FastAPI() # Uygulama nesnesi bu şekilde tanımlanmalı
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes import order, chat
app.include_router(order.router, prefix="/api")
app = FastAPI()
# Rotalar
app.include_router(chat.router, prefix="/api")

# ÖNEMLİ: Statik dosyaların yolu
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(current_dir, "frontend")

# /static/css/style.css gibi erişim sağlar
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Ürün verileri için endpoint (app.js içindeki fetch için)
@app.get("/api/products")
async def get_products():
    return FileResponse(os.path.join(current_dir, "data", "products.json"))