from pyrogram import filters, Client as Mbot
import bs4, requests
from bot import DUMP_GROUP
from apscheduler.schedulers.background import BackgroundScheduler
from sys import executable
from os import environ
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# if you are using service like heroku after restart it changes ip which avoid Ip Blocking Also Restart When Unknown Error occurred and bot is idle
RESTART_ON = environ.get('RESTART_ON')

def restart():
    try:
        execl(executable, executable, "bot.py")
    except Exception as e:
        LOGGER.error(f"Failed to restart bot: {e}")

if RESTART_ON:
    scheduler = BackgroundScheduler()
    scheduler.add_job(restart, "interval", hours=6)
    scheduler.start()

@Mbot.on_message(filters.incoming & filters.private, group=-1)
async def monitor(Mbot, message):
    if DUMP_GROUP:
        try:
            await message.forward(DUMP_GROUP)
        except Exception as e:
            LOGGER.error(f"Failed to forward message: {e}")

@Mbot.on_message(filters.command("start") & filters.incoming)
async def start(Mbot, message):
    try:
        await message.reply(f"Привет {message.from_user.mention()}\n . Я бот Фрэд! И я могу скачивать видео с Instagram, Twitter и TikTok.\nОтправь мне ссылку на видео - а я тебе ответом пришлю видео, которое ты сможешь скачать на своё устройство.")
    except Exception as e:
        LOGGER.error(f"Error in start command: {e}")
        if DUMP_GROUP:
            await Mbot.send_message(DUMP_GROUP, f"Error in start command: {e}")

@Mbot.on_message(filters.command("help") & filters.incoming)
async def help(Mbot, message):
    try:
        await message.reply("Если возникнуть проблемы напиши мне @Alex_Strayker")
    except Exception as e:
        LOGGER.error(f"Error in help command: {e}")
        if DUMP_GROUP:
            await Mbot.send_message(DUMP_GROUP, f"Error in help command: {e}")

@Mbot.on_message(filters.command("donate") & filters.incoming)
async def donate(_, message):
    try:
        await message.reply_text(f"Donate 🍪 **$**  \n**UPI**`arunrnadh2002@okhdfcbank` \n")
    except Exception as e:
        LOGGER.error(f"Error in donate command: {e}")
        if DUMP_GROUP:
            await Mbot.send_message(DUMP_GROUP, f"Error in donate command: {e}")
