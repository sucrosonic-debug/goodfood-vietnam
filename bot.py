import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import telebot
from telebot.types import InlineKeyboardMarkup, WebAppInfo, InlineKeyboardButton


BOT_TOKEN = os.environ.get("BOT_TOKEN")
MINI_APP_URL = "https://sucrosonic-debug.github.io/goodfood-vietnam/"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = telebot.TeleBot(BOT_TOKEN)


# --- Маленький сервер для Render ---

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"GoodFood Vietnam bot is running")

    def log_message(self, format, *args):
        return


def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Render health server started on port {port}", flush=True)
    server.serve_forever()


# --- Telegram ---

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            text="🍱 Открыть GoodFood",
            web_app=WebAppInfo(MINI_APP_URL)
        )
    )

    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать в GoodFood Vietnam!\n\n"
        "🥗 Собери рацион под свою цель и калорийность.\n"
        "📊 Калории и БЖУ уже рассчитаны.\n\n"
        "🇻🇳 Сейчас мы тестируем сервис в Дананге.\n\n"
        "Нажми кнопку ниже, чтобы собрать свой рацион 👇",
        reply_markup=keyboard
    )


@bot.message_handler(commands=["menu"])
def menu(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            text="🍽 Открыть мой рацион",
            web_app=WebAppInfo(MINI_APP_URL)
        )
    )

    bot.send_message(
        message.chat.id,
        "🍽 Здесь ты можешь собрать или изменить свой рацион:",
        reply_markup=keyboard
    )


@bot.message_handler(commands=["orders"])
def orders(message):
    bot.send_message(
        message.chat.id,
        "📦 Заказы появятся здесь после запуска тестовой доставки."
    )


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "❓ GoodFood Vietnam\n\n"
        "Используй /start, чтобы открыть приложение.\n\n"
        "Сейчас сервис работает в тестовом режиме 🇻🇳"
    )


if __name__ == "__main__":
    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    print("GoodFood Telegram bot started", flush=True)

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )
