import os
import asyncio
import random
from googletrans import Translator

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS

bot = Bot(token='PLACE YOUR TOKEN HERE')
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}, "
                          "ты можешь послать мне картинку, а ещё я могу перевести твоё сообщение на английский!")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help")

@dp.message(F.photo)
async def react_photo(message: Message):
    try:
        await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')
        list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
        rand_answ = random.choice(list)
        tts = gTTS(text=rand_answ, lang='ru')
        tts.save("ok.ogg")
        audio = FSInputFile("ok.ogg")
        await bot.send_voice(chat_id=message.chat.id, voice=audio)
        os.remove("ok.ogg")
    except:
        await message.answer(f"Ошибка при запросе")

# Инициализация переводчика
translator = Translator()

# Обработчик текстовых сообщений
@dp.message()
async def translate_to_english(message: Message):
    # Перевод текста на английский
    try:
        trns = translator.translate(message.text, dest='en')
        await message.answer(f"Перевод на английский:\n{trns.text}")
    except:
        await message.answer(f"Ошибка при запросе")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())