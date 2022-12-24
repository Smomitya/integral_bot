import os
from flask import Flask, request
import requests

with open('.tg_bot_token') as f:
    TG_BOT_TOKEN = next(f).strip()
with open('answers.txt') as f:
    answers = [line.strip() for line in f]

app = Flask(__name__)
users = dict()
max_score = len(os.listdir('integrals'))
if max_score != len(answers):
    raise AssertionError("Не совпадает количество заданий с количеством ответов!")


class AppUser:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.score = 0


def send_greetings(user):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    greetings = "Приветствую тебя в образовательном боте: Интегральчик - Не Забывай Как Считать Интегралы!\n" \
                "/int - решать новый интеграл\n" \
                "/ans {ответ} - отправить ответ"
    data = {"chat_id": user.chat_id, "text": greetings}
    requests.post(url, data=data)


def send_integral(user):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendPhoto"
    data = {"chat_id": user.chat_id, "caption": "Попробуй-ка взять этот интеграл"}
    files = {'photo': open(f'integrals/{user.score + 1}.png', 'rb')}
    requests.post(url, data=data, files=files)


def send_all_integrals_solved(user):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    message = "Поздравляем! Все интегралы решены. Следите за обновлениями!"
    data = {"chat_id": user.chat_id, "text": message}
    requests.post(url, data=data)


def check_answer(user, ans):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    if ans == answers[user.score]:
        message = "Правильно! Запросите новый интеграл."
        user.score += 1
    else:
        message = "Кажется, что-то не так. Проверьте свой ответ."
    data = {"chat_id": user.chat_id, "text": message}
    requests.post(url, data=data)


def send_error(user):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    message = "Не могу разобрать, используйте служебные команды."
    data = {"chat_id": user.chat_id, "text": message}
    requests.post(url, data=data)


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        print(request.json)
        chat_id = request.json['message']['chat']['id']
        text = request.json['message']['text']
        if chat_id not in users:
            user = AppUser(chat_id)
            users[chat_id] = user
            send_greetings(user)
        else:
            user = users[chat_id]
            if text == "/start":
                send_greetings(user)
            elif text == "/int":
                if user.score == max_score:
                    send_all_integrals_solved(user)
                else:
                    send_integral(user)
            elif text[:4] == "/ans" and len(text) > 4:
                check_answer(user, text[5:])
            else:
                send_error(user)

    return {"ok": True}


if __name__ == '__main__':
    app.run(host=)
