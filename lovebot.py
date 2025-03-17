import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("🚨 خطأ: لم يتم العثور على BOT_TOKEN في متغيرات البيئة!")

# تهيئة البوت
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# إعداد Webhook
WEBHOOK_HOST = "https://your-app-name.onrender.com"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))

# رسائل البوت
messages = [
    ("Hemleghkm Luna 💞", "ⵃⴻⵎⵍⴻⵖⴽⵎ ⵍⵓⵏⴰ", "I love you, Luna 💞"),
    ("أعلم أنك خائفة مما هو قادم، لكن افهميني...", "Ɛlam ad tesseḍreḍ seg wayen ara-d-yensa...", "I know you are afraid of what’s coming..."),
    ("كل هذا مقدر من البداية...", "Akk d-iserḥan seg tazwara...", "All of this was destined from the start..."),
    ("حسناً، بما أنكِ وصلتي هنا، فأنتِ في نهاية البوت...", "IH, ma teddmeḍ ɣer-d, teddmeḍ ɣer taggara n abot...", "Alright, since you've reached this point, you've reached the end of the bot...")
]

# إعداد الأزرار
def get_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("💌 التالي", callback_data="next_0"))
    return keyboard

# عند بدء المحادثة
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(messages[0][0] + "\n" + messages[0][1] + "\n" + messages[0][2], reply_markup=get_keyboard())

# عند الضغط على الزر
@dp.callback_query_handler(lambda c: c.data.startswith("next_"))
async def process_callback(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split("_")[1]) + 1
    if index < len(messages):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("💌 التالي", callback_data=f"next_{index}"))
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                    text=messages[index][0] + "\n" + messages[index][1] + "\n" + messages[index][2],
                                    reply_markup=keyboard)
    else:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                    text="💖 **نهاية البوت** 💖\n\nلقد وصلت إلى النهاية، أتمنى أن تفهمي مشاعري.")

# دوال تشغيل Webhook
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

# تشغيل Webhook
if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
)
