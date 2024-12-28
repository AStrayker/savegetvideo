import telebot
from pytube import YouTube
import os

API_TOKEN = '7529877547:AAE_55nuENDFxEk9bxOUyiPB8d6520hRoV4'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('https://www.tiktok.com/'):
        try:
            yt = YouTube(message.text)
            video = yt.streams.filter(file_extension='mp4').first()
            video.download(filename='tiktok_video.mp4')
            
            with open('tiktok_video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove('tiktok_video.mp4')  # Удаляем файл после отправки
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка: {str(e)}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте ссылку на видео из TikTok.")

bot.polling()
