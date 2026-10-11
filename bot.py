import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! 👋 Напиши сообщение — оно уйдёт администратору.")

@dp.message()
async def forward_to_admin(message: types.Message):
    user = message.from_user
    text = (
        f"📩 <b>Новое сообщение</b>\n\n"
        f"👤 {user.full_name}\n"
        f"🔗 @{user.username if user.username else 'нет'}\n"
        f"🆔 <code>{user.id}</code>\n\n"
        f"💬 {message.text or '[не текст]'}"
    )
    try:
        await bot.send_message(ADMIN_ID, text)
        if message.photo or message.document or message.video:
            await message.forward(ADMIN_ID)
        await message.answer("✅ Отправлено!")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("⚠️ Ошибка отправки.")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
