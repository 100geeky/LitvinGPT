import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from g4f.client import Client

client = Client()

logging.basicConfig(level=logging.INFO)


bot = Bot(token="YOUR_TOKEN_HERE")
dp = Dispatcher()


chat_history = {}


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здарова, меня зовут Мишаня")

@dp.message(Command("clear"))
async def cmd_clear(message: types.Message):
    chat_id = message.chat.id
    chat_history[chat_id] = []  
    await message.answer("История чата очищена!")
    with open("chat_history.json", "w", encoding='utf-8') as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=4)

@dp.message()
async def chatgpt(msg: types.Message):
    chat_id = msg.chat.id

    if chat_id not in chat_history:
        chat_history[chat_id] = []


    user_message = {"role": "user", "content": msg.text}
    chat_history[chat_id].append(user_message)

    waiting_message = await msg.answer("Ожидайте ⏳")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Ты Мишаня гпт"}, user_message],
    )

    assistant_message = {"role": "assistant", "content": response.choices[0].message.content}
    chat_history[chat_id].append(assistant_message)


    await waiting_message.edit_text(assistant_message["content"])

    with open("chat_history.json", "w", encoding='utf-8') as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=4)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
