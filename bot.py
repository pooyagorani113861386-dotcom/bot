import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# 🔑 توکن (از Railway / env)
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔒 کانال‌های اجباری
CHANNELS = [
    "@Spark_news_tel",
    "@Spark_rap",
    "@Spark_sport",
    "@Spark_hotdog"
]

# 📦 کانال آرشیو
ARCHIVE_CHANNEL = -1004336027245

# 🎬 ویدئوها
VIDEOS = {
    "video": {
        "message_id": 6
    }
}

# 🧠 چک عضویت
async def is_member(user_id: int):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

# 📢 دکمه عضویت
def join_keyboard():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📢 کانال 1", url="https://t.me/Spark_news_tel")],
        [types.InlineKeyboardButton(text="🎤 کانال 2", url="https://t.me/Spark_rap")],
        [types.InlineKeyboardButton(text="⚽️ کانال 3", url="https://t.me/Spark_sport")],
        [types.InlineKeyboardButton(text="🌭 کانال 4", url="https://t.me/Spark_hotdog")],
        [types.InlineKeyboardButton(text="🔄 تایید عضویت", callback_data="check")]
    ])

# 📥 ارسال ویدئو + حذف ۳۰ ثانیه
async def send_video(user_id: int, code: str):
    data = VIDEOS[code]

    msg = await bot.copy_message(
        chat_id=user_id,
        from_chat_id=ARCHIVE_CHANNEL,
        message_id=data["message_id"]
    )

    notice = await bot.send_message(
        user_id,
        "⏳ این ویدئو بعد از 30 ثانیه پاک خواهد شد"
    )

    await asyncio.sleep(30)

    try:
        await bot.delete_message(user_id, msg.message_id)
        await bot.delete_message(user_id, notice.message_id)
    except Exception as e:
        print("Delete error:", e)

# 🚀 استارت
@dp.message(CommandStart())
async def start(message: types.Message):
    text = message.text or ""
    parts = text.split(maxsplit=1)

    code = parts[1] if len(parts) > 1 else None

    print("START CODE:", code)

    if not code or code not in VIDEOS:
        await message.answer("❌ لینک نامعتبره")
        return

    if not await is_member(message.from_user.id):
        await message.answer(
            "❗️ برای دریافت ویدئو باید عضو همه کانال‌ها باشی 👇",
            reply_markup=join_keyboard()
        )
        return

    await send_video(message.from_user.id, code)

# 🔄 تایید عضویت
@dp.callback_query(lambda c: c.data == "check")
async def check(call: types.CallbackQuery):

    if not await is_member(call.from_user.id):
        await call.answer("❌ هنوز عضو همه کانال‌ها نیستی", show_alert=True)
        return

    await call.message.answer("✅ عضویت تایید شد")
    await send_video(call.from_user.id, "video")

# ▶️ اجرا
async def main():
    print("BOT RUNNING")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
