# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import uuid

app = FastAPI()

# Разрешаем запросы с конкретных доменов (твой сайт и адрес сервера на Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://volgatok.ru",
        "https://www.volgatok.ru",
        "https://electrobear-backend-3.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ТВОЙ AUTHORIZATION KEY (не меняй)
AUTH_KEY = "MDE5ZDlmNTYtYmY4OS03NGQyLWJkMmQtYTc4Y2M5MDA4NmY2Ojg5NTdhMWQ0LTI1MjktNGM3ZC1iMmEyLWYzZDljYmQ1MzkzMA=="

@app.post("/ask")
async def ask(request: dict):
    user_message = request.get("message", "")
    
    # 1. Получаем токен доступа
    token_res = requests.post(
        "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {AUTH_KEY}"
        },
        data="scope=GIGACHAT_API_PERS"
    )
    if token_res.status_code != 200:
        return {"reply": "Ошибка авторизации GigaChat"}

    access_token = token_res.json()["access_token"]

    # 2. Отправляем запрос к GigaChat
    chat_res = requests.post(
        "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "model": "GigaChat",
            "messages": [
                {"role": "system", "content": "Ты — ЭлектроМишка 🐻⚡. Отвечай кратко и дружелюбно, используй эмодзи."},
                {"role": "user", "content": user_message}
            ]
        }
    )
    if chat_res.status_code != 200:
        return {"reply": "Ошибка GigaChat API"}

    reply = chat_res.json()["choices"][0]["message"]["content"]
    return {"reply": reply}

# Точка входа для локального запуска (Render использует uvicorn)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
