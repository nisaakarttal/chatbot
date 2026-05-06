from fastapi import FastAPI
from routes.chat import router as chat_router
from routes.order import router as order_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(order_router)

@app.get("/")
def home():
    return {"message": "Backend çalışıyor 🚀"}