import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعداد الـ logging لتسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# جلب التوكن من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("🚨 خطأ: لم يتم العثور على BOT_TOKEN في متغيرات البيئة!")

# تهيئة البوت والموزع
bot = Bot(token=TOKEN)
dp = Dispatcher()

# رسائل البوت
messages = [
    ("Hemleghkm Luna 💞", "ⵃⴻⵎⵍⴻⵖⴽⵎ ⵍⵓⵏⴰ", "I love you, Luna 💞"),
    ("أعلم أنك خائفة مما هو قادم، لكن افهميني...", "Ɛlam ad tesseḍreḍ seg wayen ara-d-yensa...", "I know you are afraid of what’s coming..."),
    ("كل هذا مقدر من البداية...", "Akk d-iserḥan seg tazwara...", "All of this was destined from the start..."),
    ("حسناً، بما أنكِ وصلتي هنا، فأنتِ في نهاية البوت...", "IH, ma teddmeḍ ɣer-d, teddmeḍ ɣer taggara n abot...", "Alright, since you've reached this point, you've reached the end of the bot...")
]

# إعداد الأزرار
def get_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💌 التالي", callback_data="next_0")]
    ])
    return keyboard

# عند بدء المحادثة
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(messages[0][0] + "\n" + messages[0][1] + "\n" + messages[0][2], reply_markup=get_keyboard())

# عند الضغط على الزر
@dp.callback_query(lambda c: c.data.startswith("next_"))
async def process_callback(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split("_")[1]) + 1
    if index < len(messages):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💌 التالي", callback_data=f"next_{index}")]
        ])
        await callback_query.message.edit_text(messages[index][0] + "\n" + messages[index][1] + "\n" + messages[index][2], reply_markup=keyboard)
    else:
        await callback_query.message.edit_text("💖 **نهاية البوت** 💖\n\nلقد وصلت إلى النهاية، أتمنى أن تفهمي مشاعري.")

# تشغيل البوت
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
