from pyrogram import filters, Client as Mbot
import bs4, requests
from bot import DUMP_GROUP
from apscheduler.schedulers.background import BackgroundScheduler
from sys import executable
from os import sys, execl, environ

# if you are using service like heroku after restart it changes ip which avoid Ip Blocking Also Restart When Unknown Error occurred and bot is idle
RESTART_ON = environ.get('RESTART_ON')

def restart():
    execl(executable, executable, "bot.py")

if RESTART_ON:
    scheduler = BackgroundScheduler()
    scheduler.add_job(restart, "interval", hours=6)
    scheduler.start()

@Mbot.on_message(filters.incoming & filters.private, group=-1)
async def monitor(Mbot, message):
    if DUMP_GROUP:
        await message.forward(DUMP_GROUP)

@Mbot.on_message(filters.command("start") & filters.incoming)
async def start(Mbot, message):
    await message.reply(f"Привет {message.from_user.mention()}\n . Я бот Фрэд! И я могу скачивать видео с Instagram, Twitter и TikTok.
Отправь мне ссылку на видео - а я тебе ответом пришлю видео, которое ты сможешь скачать на своё устройство ")

@Mbot.on_message(filters.command("help") & filters.incoming)
async def help(Mbot, message):
    await message.reply("Если возникнуть проблемы напиши мне @Alex_Strayker")

@Mbot.on_message(filters.command("donate") & filters.command("Donate") & filters.incoming)
async def donate(_, message):
    await message.reply_text(f"Donate 🍪 **$** https://www.buymeacoffee.com/Masterolic \n**UPI**`arunrnadh2002@okhdfcbank` \nhttps://www.paypal.me/MasterolicOfficial")
