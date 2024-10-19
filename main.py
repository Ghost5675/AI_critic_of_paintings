from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from assistent import generate_assistant_message  # Импортируем логику ассистента

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
