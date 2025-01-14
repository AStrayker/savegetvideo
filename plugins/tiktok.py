from pyrogram import filters, Client as Mbot
import bs4, requests, re, asyncio
import wget, os, traceback
from bot import LOG_GROUP, DUMP_GROUP

@Mbot.on_message(filters.regex(r'https?://.*tiktok[^\s]+') & filters.incoming)
async def link_handler(Mbot, message):
    link = message.matches[0].group(0)
    try:
        # Отправка стикера в ответ на сообщение пользователя
        m = await message.reply_sticker("CAACAgIAAxkBATWhF2Qz1Y-FKIKqlw88oYgN8N82FtC8AAJnAAPb234AAT3fFO9hR5GfHgQ")
        
        # Получение данных от API
        get_api = requests.post("https://lovetik.com/api/ajax/search", data={"query": link}).json()
        
        if get_api['status'] and "Invalid TikTok video url" in get_api['mess']:
            return await message.reply("Oops Invalid TikTok video url. Please try again :) ")
        
        if get_api.get('links'):
            try:
                video_url = get_api['links'][0]['a']
                if "MP3" in get_api['links'][0]['t']:
                    try:
                        await message.reply_photo(get_api['cover'])
                    except:
                        pass
                
                # Отправка видео в ответ на сообщение пользователя
                dump_file = await message.reply_video(video_url, caption="Thank you for using - @InstaReelsdownbot")
                
                # Копирование видео в DUMP_GROUP
                if DUMP_GROUP:
                    await dump_file.copy(DUMP_GROUP)
                
                # Возврат после успешной отправки, чтобы предотвратить дальнейшее выполнение
                return
            except KeyError:
                await message.reply("Invalid TikTok video url. Please try again.")
            except Exception as e:
                print(f"Error sending video: {e}")
                if LOG_GROUP:
                    await Mbot.send_message(LOG_GROUP, f"TikTok {e} {link}")
                    await Mbot.send_message(LOG_GROUP, traceback.format_exc())
    except Exception as e:
        if LOG_GROUP:
            await Mbot.send_message(LOG_GROUP, f"TikTok {e} {link}")
            await Mbot.send_message(LOG_GROUP, traceback.format_exc())
    finally:
        # Удаление стикера
        await m.delete()
        # Отправка сообщения с рекламой других ботов
        await message.reply(
            "Check out @spotify_downloa_bot(music)  @spotifynewss(Channel) \n Please Support Us By /donate To Maintain This Project")
