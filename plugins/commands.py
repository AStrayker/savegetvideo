from aiogram import Bot, Dispatcher, F
from aiogram.types import BufferedInputFile, Message
from settings import settings
from tiktok.api import TikTokAPI
import time

dp = Dispatcher()

filters = [
    F.text.contains("tiktok.com"),
    (not settings.allowed_ids)
    | F.chat.id.in_(settings.allowed_ids)
    | F.from_user.id.in_(settings.allowed_ids),
]

# Словарь для отслеживания последнего времени отправки сообщения для каждого пользователя
last_message_time = {}

@dp.message(*filters)
@dp.channel_post(*filters)
async def handle_tiktok_request(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id if message.from_user else message.chat.id
    current_time = time.time()
    
    # Проверяем, не отправляли ли мы сообщение этому пользователю недавно
    if user_id in last_message_time and (current_time - last_message_time[user_id]) < 10:  # 10 секунд таймаут
        return  # Если да, то пропускаем обработку
    
    entries = [
        message.text[e.offset : e.offset + e.length]
        for e in message.entities or []
        if message.text is not None
    ]

    urls = [
        u if u.startswith("http") else f"https://{u}"
        for u in filter(lambda e: "tiktok.com" in e, entries)
    ]

    async for tiktok in TikTokAPI.download_tiktoks(urls):
        if not tiktok.video:
            continue

        video = BufferedInputFile(tiktok.video, filename="video.mp4")
        caption = tiktok.caption if settings.with_captions else None

        if settings.reply_to_message:
            await message.reply_video(video=video, caption=caption)
        else:
            await bot.send_video(chat_id=message.chat.id, video=video, caption=caption)
    
    # Отмечаем время отправки сообщения
    last_message_time[user_id] = current_time
