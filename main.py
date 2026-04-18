**from fastapi import FastAPI**

**from fastapi.middleware.cors import CORSMiddleware**

**import requests**

**import uuid**



**app = FastAPI()**



**app.add\_middleware(**

&#x20;   **CORSMiddleware,**

&#x20;   **allow\_origins=\["\*"],**

&#x20;   **allow\_methods=\["\*"],**

&#x20;   **allow\_headers=\["\*"],**

**)**



**AUTH\_KEY = "MDE5ZDlmNTYtYmY4OS03NGQyLWJkMmQtYTc4Y2M5MDA4NmY2Ojg5NTdhMWQ0LTI1MjktNGM3ZC1iMmEyLWYzZDljYmQ1MzkzMA=="**



**@app.post("/ask")**

**async def ask(request: dict):**

&#x20;   **user\_message = request.get("message", "")**

&#x20;   **token\_res = requests.post(**

&#x20;       **"https://ngw.devices.sberbank.ru:9443/api/v2/oauth",**

&#x20;       **headers={**

&#x20;           **"Content-Type": "application/x-www-form-urlencoded",**

&#x20;           **"Accept": "application/json",**

&#x20;           **"RqUID": str(uuid.uuid4()),**

&#x20;           **"Authorization": f"Basic {AUTH\_KEY}"**

&#x20;       **},**

&#x20;       **data="scope=GIGACHAT\_API\_PERS"**

&#x20;   **)**

&#x20;   **if token\_res.status\_code != 200:**

&#x20;       **return {"reply": "Ошибка авторизации"}**

&#x20;   **access\_token = token\_res.json()\["access\_token"]**

&#x20;   **chat\_res = requests.post(**

&#x20;       **"https://gigachat.devices.sberbank.ru/api/v1/chat/completions",**

&#x20;       **headers={**

&#x20;           **"Content-Type": "application/json",**

&#x20;           **"Authorization": f"Bearer {access\_token}"**

&#x20;       **},**

&#x20;       **json={**

&#x20;           **"model": "GigaChat",**

&#x20;           **"messages": \[**

&#x20;               **{"role": "system", "content": "Ты — ЭлектроМишка 🐻⚡. Отвечай кратко."},**

&#x20;               **{"role": "user", "content": user\_message}**

&#x20;           **]**

&#x20;       **}**

&#x20;   **)**

&#x20;   **if chat\_res.status\_code != 200:**

&#x20;       **return {"reply": "Ошибка GigaChat"}**

&#x20;   **reply = chat\_res.json()\["choices"]\[0]\["message"]\["content"]**

&#x20;   **return {"reply": reply}**



**if \_\_name\_\_ == "\_\_main\_\_":**

&#x20;   **import uvicorn**

&#x20;   **uvicorn.run(app, host="0.0.0.0", port=8000)**

