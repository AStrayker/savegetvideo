from pyrogram import filters, Client as Mbot
from os import mkdir, environ
from random import randint
from bot import LOG_GROUP, DUMP_GROUP
from yt_dlp import YoutubeDL
from requests import get
import os, traceback

FIXIE_SOCKS_HOST = environ.get('FIXIE_SOCKS_HOST')

async def thumb_down(videoId):
    with open(f"/tmp/{videoId}.jpg", "wb") as file:
        file.write(get(f"https://img.youtube.com/vi/{videoId}/default.jpg").content)
    return f"/tmp/{videoId}.jpg"

async def ytdl_video(path, video_url, id):
    file = f"{path}/%(title)s.%(ext)s"
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": file,
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "cache-dir": "/tmp/",
        "nocheckcertificate": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            video = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(video)
            return filename
        except Exception as e:
            if FIXIE_SOCKS_HOST:
                ydl_opts['proxy'] = f"socks5://{FIXIE_SOCKS_HOST}"
                with YoutubeDL(ydl_opts) as ydl:
                    try:
                        video = ydl.extract_info(video_url, download=True)
                        filename = ydl.prepare_filename(video)
                        return filename
                    except Exception as e:
                        print(e)
            else:
                print(e)

@Mbot.on_message(filters.regex(r'https?://.*youtube[^\s]+') & filters.incoming | filters.regex(r'(https?:\/\/(?:www\.)?youtu\.?be(?:\.com)?\/.*)') & filters.incoming)
async def _(Mbot, message):
    try:
        m = await message.reply_sticker("CAACAgIAAxkBATWhF2Qz1Y-FKIKqlw88oYgN8N82FtC8AAJnAAPb234AAT3fFO9hR5GfHgQ")
    except:
        pass
    link = message.matches[0].group(0)
    if "channel" in link or "/c/" in link:
        return await m.edit_text("**Channel** Download Not Available.")
    if "shorts" in link:
        try:
            randomdir = "/tmp/" + str(randint(1, 100000000))
            mkdir(randomdir)
            fileLink = await ytdl_video(randomdir, link, message.from_user.id)
            AForCopy = await message.reply_video(fileLink)
            if os.path.exists(randomdir):
                rmtree(randomdir)
            await m.delete()
            if DUMP_GROUP:
                await AForCopy.copy(DUMP_GROUP)
        except Exception as e:
            await m.delete()
            if LOG_GROUP:
                await Mbot.send_message(LOG_GROUP, f"YouTube Shorts {e} {link}")
                await message.reply(f"400: Sorry, Unable To Find It  try another or report it  to @masterolic or support chat @spotify_supportbot 🤖")
                await Mbot.send_message(LOG_GROUP, traceback.format_exc())
        return await message.reply("Check out @spotify_downloa_bot(music)  @spotifynewss(Channel) \n Please Support Us By /donate To Maintain This Project")
    try:
        if "music.youtube.com" in link:
            link = link.replace("music.youtube.com", "youtube.com")
        ids = await getIds(link)
        randomdir = "/tmp/" + str(randint(1, 100000000))
        mkdir(randomdir)
        for id in ids:
            link = f"https://youtu.be/{id[0]}"
            PForCopy = await message.reply_photo(f"https://i.ytimg.com/vi/{id[0]}/hqdefault.jpg", caption=f"🎧 Title : `{id[3]}`\n🎤 Artist : `{id[2]}`\n💽 Track No : `{id[1]}`\n💽 Total Track : `{len(ids)}`")
            fileLink = await ytdl_down(randomdir, link, message.from_user.id)
            thumnail = await thumb_down(id[0])
            AForCopy = await message.reply_audio(fileLink, caption=f"[{id[3]}](https://youtu.be/{id[0]}) - {id[2]} Thank you for using - @InstaReelsdownbot", title=id[3].replace("_", " "), performer=id[2])
            if DUMP_GROUP:
                await PForCopy.copy(DUMP_GROUP)
                await AForCopy.copy(DUMP_GROUP)
        await m.delete()
        if os.path.exists(randomdir):
            rmtree(randomdir)
        await message.reply("Check out @spotify_downloa_bot(music)  @spotifynewss(Channel) \n Please Support Us By /donate To Maintain This Project")
    except Exception as e:
        if LOG_GROUP:
            await Mbot.send_message(LOG_GROUP, f"Youtube {e} {link}")
            await message.reply(f"400: Sorry, Unable To Find It  try another or report it  to @masterolic or support chat @spotify_supportbot 🤖")
            await Mbot.send_message(LOG_GROUP, traceback.format_exc())
