import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

کانال‌های عضویت اجباری

CHANNELS = [
"@Spark_news_tel",
"@Spark_rap",
"@Spark_sport",
"@Spark_hotdog"
]

کانال آرشیو

ARCHIVE_CHANNEL = -1004336027245

پیام فایل داخل کانال آرشیو

FILE_MESSAGE_ID = 6

async def is_member(user_id: int):
for ch in CHANNELS:
try:
member = await bot.get_chat_member(ch, user_id)

        if member.status in ["left", "kicked"]:
            return False

    except Exception:
        return False

return True

def join_keyboard():
return types.InlineKeyboardMarkup(
inline_keyboard=[
[types.InlineKeyboardButton(
text="📢 کانال خبر",
url="https://t.me/Spark_news_tel"
)],
[types.InlineKeyboardButton(
text="🎤 کانال رپ",
url="https://t.me/Spark_rap"
)],
[types.InlineKeyboardButton(
text="⚽ کانال ورزش",
url="https://t.me/Spark_sport"
)],
[types.InlineKeyboardButton(
text="🌭 کانال هات‌داگ",
url="https://t.me/Spark_hotdog"
)],
[types.InlineKeyboardButton(
text="🔄 تایید عضویت",
callback_data="check"
)]
]
)

async def send_file(user_id: int):
file_msg = await bot.copy_message(
chat_id=user_id,
from_chat_id=ARCHIVE_CHANNEL,
message_id=FILE_MESSAGE_ID
)

notice = await bot.send_message(
    user_id,
    "⏳ این فایل بعد از ۳۰ ثانیه حذف می‌شود."
)

await asyncio.sleep(30)

try:
    await bot.delete_message(user_id, file_msg.message_id)
    await bot.delete_message(user_id, notice.message_id)
except Exception as e:
    print("Delete Error:", e)

@dp.message(CommandStart())
async def start(message: types.Message):

if not await is_member(message.from_user.id):

    await message.answer(
        "❗ برای دریافت فایل ابتدا عضو کانال‌ها شو 👇",
        reply_markup=join_keyboard()
    )
    return

await send_file(message.from_user.id)

@dp.callback_query(lambda c: c.data == "check")
async def check(call: types.CallbackQuery):

if not await is_member(call.from_user.id):
    await call.answer(
        "❌ هنوز عضو همه کانال‌ها نیستی",
        show_alert=True
    )
    return

await call.answer("✅ عضویت تایید شد")

await send_file(call.from_user.id)

async def main():
print("BOT RUNNING")
await dp.start_polling(bot)

if name == "main":
asyncio.run(main())
