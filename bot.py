import os
import telebot
from telebot.types import InlineKeyboardMarkup, WebAppInfo, InlineKeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

MINI_APP_URL = "https://sucrosonic-debug.github.io/goodfood-vietnam/"


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = InlineKeyboardMarkup()

    open_app = InlineKeyboardButton(
        text="🍱 Открыть GoodFood",
        web_app=WebAppInfo(MINI_APP_URL)
    )

    keyboard.add(open_app)

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


print("GoodFood bot started")

bot.infinity_polling()
