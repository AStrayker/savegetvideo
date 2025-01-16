from pyrogram import filters, Client as Mbot
import bs4, requests
from bot import DUMP_GROUP
from apscheduler.schedulers.background import BackgroundScheduler
from sys import executable
from os import execl, environ

# Если вы используете сервис вроде Heroku, после перезапуска меняется IP, что помогает избежать блокировки IP. Также перезапуск при неизвестной ошибке и когда бот простаивает.
RESTART_ON = environ.get('RESTART_ON')

def restart():
    execl(executable, executable, "bot.py")

if RESTART_ON:
    scheduler = BackgroundScheduler()
    scheduler.add_job(restart, "interval", hours=6)
    scheduler.start()

# Словарь для отслеживания пользователей, которым уже отправлено приветствие
greeted_users = {}

@Mbot.on_message(filters.incoming & filters.private, group=-1)
async def monitor(Mbot, message):
    if DUMP_GROUP:
        await message.forward(DUMP_GROUP)

@Mbot.on_message(filters.command("start") & filters.incoming)
async def start(Mbot, message):
    user_id = message.from_user.id
    # Проверяем, был ли уже отправлен приветственный текст этому пользователю
    if user_id not in greeted_users:
        await message.reply(f"Hello 👋👋 {message.from_user.mention()}\nI am A Simple Telegram Bot Can Download From Multiple Social Media Currently Support Instagram, TikTok, Twitter, Facebook, YouTube(Music and shorts) And So On....!")
        # Помечаем пользователя как приветствованного
        greeted_users[user_id] = True
    else:
        # Если пользователь уже был приветствован, ничего не делаем
        pass

@Mbot.on_message(filters.command("help") & filters.incoming)
async def help(Mbot, message):
    await message.reply("This is user friendly bot so you can simple send your Instagram reel and post links here:) \n eg: `https://www.instagram.com/reel/CZqWDGODoov/?igshid=MzRlODBiNWFlZA==`\n `post:` `https://www.instagram.com/reel/CuCTtORJbDj/?igshid=MzRlODBiNWFlZA==`")

@Mbot.on_message(filters.command("donate") & filters.command("Donate") & filters.incoming)
async def donate(_, message):
    await message.reply_text(f"Donate 🍪 **$** https://www.buymeacoffee.com/Masterolic \n**UPI** `arunrnadh2002@okhdfcbank` \nhttps://www.paypal.me/MasterolicOfficial")
