from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes.chat import router as chat_router
"""main.py, backend’i başlatır, API route’ları bağlar ve frontend dosyalarını servis ederek tüm sistemi ayağa kaldırır."""

"""FastAPI uygulamasını oluşturur"""
app = FastAPI()

"""[cors ayarı]Frontend-backend iletişimi açılıyor"""
"""Frontend (React vs) backend’e rahatça bağlanabilsin diye:
API erişimini açar
“izin sistemi” gibi düşün"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Chat endpoint’lerini projeye ekler:
/api/chat artık aktif olur"""

app.include_router(chat_router)

app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")
app.mount("/data", StaticFiles(directory="frontend/data"), name="data")
app.mount("/images", StaticFiles(directory="frontend/static/images"), name="images")
"""Frontend dosyalarını servis eder"""

"""Ana sayfa açılır"""
@app.get("/")
def root():
    return FileResponse("frontend/index.html")