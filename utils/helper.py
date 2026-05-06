from datetime import datetime

def log(type, message):
    print(f"[{datetime.now()}] [{type}] {message}")

def ai_log(message):
    log("AI", message)

def request_log(message):
    log("REQUEST", message)

def error_log(message):
    log("ERROR", message)