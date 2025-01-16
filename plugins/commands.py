from pyrogram import filters, Client as Mbot
import sqlite3
import os
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

# Функция для работы с базой данных
def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS greeted_users
                      (user_id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()

def user_greeted(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM greeted_users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_user_as_greeted(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO greeted_users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

# Инициализация базы данных при старте бота
init_db()

@Mbot.on_message(filters.incoming & filters.private, group=-1)
async def monitor(Mbot, message):
    if DUMP_GROUP:
        await message.forward(DUMP_GROUP)

@Mbot.on_message(filters.command("start") & filters.incoming)
async def start(Mbot, message):
    user_id = message.from_user.id
    if not user_greeted(user_id):
        await message.reply(f"Hello 👋👋 {message.from_user.mention()}\nI am A Simple Telegram Bot Can Download From Multiple Social Media Currently Support Instagram, TikTok, Twitter, Facebook, YouTube(Music and shorts) And So On....!")
        mark_user_as_greeted(user_id)
    else:
        # Если пользователь уже был приветствован, просто игнорируем команду
        pass

@Mbot.on_message(filters.command("help") & filters.incoming)
async def help(Mbot, message):
    await message.reply("This is user friendly bot so you can simple send your Instagram reel and post links here:) \n eg: `https://www.instagram.com/reel/CZqWDGODoov/?igshid=MzRlODBiNWFlZA==`\n `post:` `https://www.instagram.com/reel/CuCTtORJbDj/?igshid=MzRlODBiNWFlZA==`")

@Mbot.on_message(filters.command("donate") & filters.command("Donate") & filters.incoming)
async def donate(_, message):
    await message.reply_text(f"Donate 🍪 **$** https://www.buymeacoffee.com/Masterolic \n**UPI** `arunrnadh2002@okhdfcbank` \nhttps://www.paypal.me/MasterolicOfficial")
