import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعداد تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# جلب التوكن من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("🚨 خطأ: لم يتم العثور على BOT_TOKEN في متغيرات البيئة!")

# تهيئة البوت والموزع
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 📝 **جميع الرسائل العشر كاملة باللغة العربية فقط + الإضافة الأخيرة**
messages = [
    "Hemleghkm luna 💞\n\n"
    "أنتِ مثل القمر، تضيئين السماء وتنيرين حياتي، Luna 💞\n"
    "القمر يظل دائمًا في السماء، وأنتِ دائمًا في قلبي، مثل Luna تحت ضوء الليل.",

    "أعلم أنك خائفة مما هو قادم، لكن افهميني، لقد التقيت بك صغيرة في الثانوية ولم أرد إضاعتك من يدي لأنك فتاة مثالية بالنسبة لي، مثل القمر الذي يظهر مرة كل ليلة، ولا أريد أن أغفل عنه أبدًا.",

    "من حقك الخوف، لكن لدينا الله. من فضلك، لنكمل حتى آخر لحظة، فأنا انتظرتك كثيرًا، وفقدانك مؤلم ومؤذٍ لي جدًا.\n"
    "أعرف أنكِ لستِ بأفضل حال، فاتخاذ قرار كهذا صعب جدًا، لكني أفهم رغبتك في حماية نفسكِ ونفسيتكِ.\n"
    "لكني أخبرتكِ أني لستُ شخصًا يلعب بكِ، وإنما أردتُ أن أكمل حياتي معكِ، وأعيش كل لحظاتها معكِ، وأحقق طموحاتي، وأنتِ موجودة في كل خططي.",

    "كانت 4 أشهر فقط، لكن مرت بالنسبة لي كالسنوات. شاركنا معًا الكثير من القصص، الفرح، والأحزان.\n"
    "أعرف أنكِ خائفة، ولا تستطيعين وضع ثقتك بسهولة. تخشين أن يتم كسرك وإيذاؤك، لكني سأفعل أي شيء لحمايتك ومنع الحزن عنكِ.\n"
    "أنا هنا فقط لأجلكِ، لجعلكِ سعيدة، لإرضائكِ، وخدمتكِ. إذا شعرتِ بالتعب مني أو من علاقتنا، خذي استراحة واطلبيها مني، لكن لا تقطعي علاقتنا للأبد.",

    "كل هذا مقدر من البداية، وأحساسي يقول إنه كُتب لنا أن نكون معًا. فقط الله يختبر طريقة سعينا للأمر، لأنه لا يضع شيئًا في القلوب إلا وهو يعلم بأنه سيتحقق، لكن يجب على الإنسان أن يعيده ويطيعه ويقوم بالدعاء.\n"
    "شعورنا واحد، ونريد الحلال فقط. لنكمل حتى آخر لحظة، والله معنا، لكن عليكِ وضع السجادة والقيام بالدعاء.",

    "أرجو منكِ تفهم مشاعري تجاهك، أنا صادق في قولي، وحقًا سيكون مؤلمًا ومؤذيًا لي أن تتركيني.\n"
    "لونا، أحبكِ حبًا كبيرًا، ولن أؤذيكِ.\n"
    "أما عن القدر، فدعاؤنا واستمرارنا في علاقتنا رغم كل شيء سيحقق لنا مرادنا.",

    "لذا من فضلك، أنا أترجاكِ يا ذات الوجه الجميل والقلب الصخري 🥲💔🪨، أرجوكِ لا تتركيني.\n"
    "من فضلك، أسأل الله أن يجازيكِ ويحفظكِ لفعلتكِ، ولن أنسى طالما بقيت حيًا.\n"
    "أرجوكِ لونا، أنا أحبكِ، لا تذهبي.",

    "أرجو أن تتفهمي إصراري على بقائكِ، سأقف دوماً بجانبكِ وأتفهمكِ دائمًا، لكن لا تذهبي، هذا طلبي، أرجوكِ 🙏\n"
    "أرجوكِ، سأبقى أحاول حتى نعود، حتى لو بعد 5 سنوات، سأرسل طلب متابعة لإنستا الخاص بكِ، أنا لا أقبلكِ إلا أنتِ.\n"
    "أحبكِ حقًا من قلبي، أرجو أن تقدّري مشاعري ولا ترفضي طلبي، فهذا سيكسرني ويحطمني حقًا. من فضلكِ لونا.",

    "حسنا، بما أنكِ وصلتي هنا، فأنتِ في نهاية البوت. لقد قمت ببرمجته بالهاتف، لذا أرجو أن يشتغل بشكل جيد! 🙂\n"
    "لقد عبرت عن مشاعري ورأيي الصريح فيه، أتمنى تفهمكِ وأن تقبلي بي من جديد ونستمر. هذه المشاكل والعقبات تظهر في أي علاقة، لكن علينا أن نستمر.\n"
    "'امحي الغلطة والمشكل علاجال علاقتنا، ومشي تمحي العلاقة علاجال المشكل والغلطة.' — الفيلسوف إسلام.",

    "**ayen ak imxdmegh**"
]

# إعداد الأزرار
def get_keyboard(index):
    if index < len(messages) - 1:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💌 التالي", callback_data=f"next_{index + 1}")]
        ])
    else:
        keyboard = None
    return keyboard

# بدء المحادثة
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(messages[0], reply_markup=get_keyboard(0))

# التنقل بين الرسائل
@dp.callback_query(lambda c: c.data.startswith("next_"))
async def process_callback(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split("_")[1])
    await callback_query.message.edit_text(messages[index], reply_markup=get_keyboard(index))

# تشغيل البوت
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
