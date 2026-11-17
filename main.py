from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

LOG_FILE = Path("notifications.log")

class Feedback(BaseModel):
    name : str
    message : str

def save_notification(name: str, message: str):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Message: {message}\n")
        file.write("-" *30 + "\n")


@app.post("/feedback")
def create_feedback( feedback: Feedback, background_tasks: BackgroundTasks ):
    background_tasks.add_task( save_notification, feedback.name, feedback.message )
    return{ "message" : "Feedback received successfully", "name" : feedback.name }

@app.get("/feedback/logs")
def get_feedback_logs():
    if not LOG_FILE.exists():
        return {"logs" : "No notifications yet"} #возвращаем сообщение, что уведомлений пока нет
    with open(LOG_FILE, "r" , encoding="utf-8") as file: #Здесь открываем файл в режиме "r" — чтение
        content = file.read()
    return {"logs" : content}


#BaseModel описывает и проверяет структуру входящих данных
# "a" в open() - добавляет данные в конец файла
# background_tasks.add_task() добавляет функцию для последующего фонового выполнения
# Мы передаем save_notification для последующего вызова, а не вызываем ее сразу