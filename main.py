from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from assistent import generate_assistant_message  # Импортируем логику ассистента
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
import requests
import os

OPEN_AI_API = ''
app = FastAPI()

# Подключаем шаблоны и статику
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    text: str


@app.get("/")
async def get_chat_page(request: Request):
    # При загрузке страницы ассистент отправляет первое сообщение
    assistant_first_message = generate_assistant_message()
    return templates.TemplateResponse("index.html", {"request": request, "assistant_first_message": assistant_first_message})


@app.post("/send_message/")
async def send_message(message: Message):
    # Проверяем, что сообщение передано
    if not message.text:
        return {"response": "Ошибка: сообщение пустое"}

    # Получаем ответ от ассистента
    response_text = generate_assistant_message(message.text)

    # Проверяем, что ответ не пуст
    if not response_text:
        return {"response": "Ошибка: ассистент не смог сгенерировать ответ"}

    return {"response": response_text}


@app.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    
    try:
        # Декодируем Base64 строку
        image_data = base64.b64decode(image)

        # Сохраняем изображение (по желанию)
        with open("uploaded_image.png", "wb") as f:
            f.write(image_data)

        # Отправляем изображение в OpenAI API для анализа
        response = openai.Image.create(
            model="gpt-4o-mini",  # Замените на вашу модель
            prompt="Предоставьте критику для этого изображения.",  # Ваш запрос к модели
            files={"file": ("uploaded_image.png", image_data, "image/png")},
        )

        critique = response.get("data", [{}])[0].get("text")  # Измените на соответствующее поле, которое возвращает OpenAI
        return JSONResponse(content={"result": critique})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={"result": "Изображение загружено успешно"})
