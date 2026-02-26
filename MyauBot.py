import logging
import asyncio
import sys
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import WebAppInfo, MenuButtonWebApp
from aiogram.utils.token import TokenValidationError

# Импортируем dotenv для безопасного хранения ключей
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# --- КОНФИГУРАЦИЯ ---
# На GitHub мы не пишем токен напрямую!
# Создай файл .env в этой же папке и напиши там: BOT_TOKEN=твой_токен
BOT_TOKEN = os.getenv("BOT_TOKEN") or "8748623574:AAGMkdJ7Gj8IxVcca81zm5_At-ejbq12Ehc"

# Ссылка на твой развернутый React-интерфейс (Vercel/Netlify)
WEB_APP_URL = os.getenv("WEB_APP_URL") or "https://твой-сайт-на-vercel.app"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация бота с проверкой токена
try:
    if not BOT_TOKEN or BOT_TOKEN == "ВАШ_ТЕЛЕГРАМ_ТОКЕН":
        raise TokenValidationError("Token is missing")
    bot = Bot(token=BOT_TOKEN)
except TokenValidationError:
    print("\n❌ ОШИБКА: Токен не найден или неверный!")
    print("Если вы запускаете локально, создайте файл .env и добавьте туда BOT_TOKEN.")
    sys.exit(1)

dp = Dispatcher()


# --- ОБРАБОТЧИКИ КОМАНД ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Приветствие и запуск Web App."""
    user_name = message.from_user.first_name or "Друг"

    welcome_text = (
        f"🐾 <b>Мур, {user_name}!</b>\n\n"
        f"Добро пожаловать в элитную нейро-студию <b>Myau Photo Pro</b>.\n\n"
        f"💠 <b>Движок:</b> Nano Banana Pro v2.5\n"
        f"💠 <b>Качество:</b> Ultra HD (8K)\n"
        f"💠 <b>Модель:</b> Gemini 2.5 Flash Image Preview\n\n"
        f"Нажми на кнопку ниже, чтобы запустить систему!"
    )

    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(
            text="🚀 ЗАПУСТИТЬ NANO STUDIO",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )
    )
    builder.row(
        types.KeyboardButton(text="📜 Инфо"),
        types.KeyboardButton(text="💎 Статус")
    )

    await message.answer(
        welcome_text,
        parse_mode="HTML",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

    # Установка кнопки меню WebApp
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(
            text="📸 Studio",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )
    )


@dp.message(lambda message: message.text == "📜 Инфо")
async def info_handler(message: types.Message):
    info_text = (
        "📊 <b>Техническая спецификация Myau Photo Pro:</b>\n\n"
        "• <b>Ядро:</b> Nano Banana Pro Engine\n"
        "• <b>API:</b> Google Generative AI v1beta\n"
        "• <b>Интерфейс:</b> React + Tailwind CSS\n"
        "• <b>База данных:</b> Firebase Firestore\n"
        "• <b>Лимит:</b> 15 генераций в сутки"
    )
    await message.answer(info_text, parse_mode="HTML")


@dp.message(lambda message: message.text == "💎 Статус")
async def status_handler(message: types.Message):
    status_text = (
        "✅ <b>Статус систем:</b>\n\n"
        "🌐 Сервер: <code>Online</code>\n"
        "⚡ Nano Pro Engine: <code>Active</code>\n"
        "🧠 AI Model: <code>Ready</code>"
    )
    await message.answer(status_text, parse_mode="HTML")


@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(
        "🐾 Мур! Нажми на кнопку <b>'ЗАПУСТИТЬ NANO STUDIO'</b>, чтобы начать работу.",
        parse_mode="HTML"
    )


# --- ЗАПУСК БОТА ---

async def main():
    print("-------------------------------------------")
    print("   MYAU PHOTO PRO (PYTHON) IS STARTING    ")
    print(f"   Target URL: {WEB_APP_URL}             ")
    if "vercel.app" in WEB_APP_URL and "твой-сайт" in WEB_APP_URL:
        print("   ⚠️ ВНИМАНИЕ: Замени WEB_APP_URL на реальный адрес!")
    print("-------------------------------------------")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nБот остановлен.")