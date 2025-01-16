from pyrogram import filters, Client as Mbot
from bot import LOG_GROUP, DUMP_GROUP
import os, re, asyncio, bs4
import requests, wget, traceback

@Mbot.on_message(filters.regex(r'https?://.*twitter[^\s]+') & filters.incoming | filters.regex(r'https?://(?:www\.)?x\.com/\S+') & filters.incoming, group=-5)
async def twitter_handler(Mbot, message):
    try:
        link = message.matches[0].group(0)
        if "x.com" in link:
            link = link.replace("x.com", "fxtwitter.com")
        elif "twitter.com" in link:
            link = link.replace("twitter.com", "fxtwitter.com")
        m = await message.reply_sticker("CAACAgIAAxkBATWhF2Qz1Y-FKIKqlw88oYgN8N82FtC8AAJnAAPb234AAT3fFO9hR5GfHgQ")
        try:
            dump_file = await message.reply_video(link, caption="Thank you for using - @InstaReelsdownbot")
            if DUMP_GROUP:
                await dump_file.copy(DUMP_GROUP)
        except Exception as e:
            snd_message = await message.reply(link)
            await asyncio.sleep(1)
            try:
                dump_file = await message.reply_video(link, caption="Thank you for using - @InstaReelsdownbot")
                await snd_message.delete()
                if DUMP_GROUP:
                    await dump_file.copy(DUMP_GROUP)
            except Exception as e:
                await snd_message.delete
