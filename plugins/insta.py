from pyrogram import filters, Client as Mbot
import bs4, requests, re, asyncio
import os, traceback, random
from bot import LOG_GROUP, DUMP_GROUP

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "99",
    "Origin": "https://saveig.app",
    "Connection": "keep-alive",
    "Referer": "https://saveig.app/en",
}

@Mbot.on_message(filters.regex(r'https?://.*instagram[^\s]+') & filters.incoming)
async def link_handler(Mbot, message):
    link = message.matches[0].group(0)
    global headers
    try:
        m = await message.reply_sticker("CAACAgIAAxkBATWhF2Qz1Y-FKIKqlw88oYgN8N82FtC8AAJnAAPb234AAT3fFO9hR5GfHgQ")
        url = link.replace("instagram.com", "ddinstagram.com").replace("==", "%3D%3D")
        if url.endswith("="):
            dump_file = await message.reply_video(url[:-1], caption="Thank you for using - @InstaReelsdownbot")
        else:
            dump_file = await message.reply_video(url, caption="Thank you for using - @InstaReelsdownbot")
        if DUMP_GROUP:
            await dump_file.forward(DUMP_GROUP)
        await m.delete()
    except Exception as e:
        try:
            if "/reel/" in url:
                ddinsta = True
                getdata = requests.get(url).text
                soup = bs4.BeautifulSoup(getdata, 'html.parser')
                meta_tag = soup.find('meta', attrs={'property': 'og:video'})
                try:
                    content_value = f"https://ddinstagram.com{meta_tag['content']}"
                except:
                    pass
                if not meta_tag:
                    ddinsta = False
                    meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
                    if meta_tag.ok:
                        res = meta_tag.json()
                        meta = re.findall(r'href="(https?://[^"]+)"', res['data'])
                        content_value = meta[0]
                    else:
                        return await message.reply("oops something went wrong")
                if ddinsta:
                    dump_file = await message.reply_video(content_value, caption="Thank you for using - @InstaReelsdownbot")
                else:
                    dump_file = await message.reply_video(content_value, caption="Thank you for using - @InstaReelsdownbot")
                if DUMP_GROUP:
                    await dump_file.copy(DUMP_GROUP)
            elif "/p/" in url:
                meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
                if meta_tag.ok:
                    res = meta_tag.json()
                    meta = re.findall(r'href="(https?://[^"]+)"', res['data'])
                else:
                    return await message.reply("oops something went wrong")
                for i in range(len(meta) - 1):
                    com = await message.reply_text(meta[i])
                    await asyncio.sleep(1)
                    try:
                        dump_file = await message.reply_video(com.text, caption="Thank you for using - @InstaReelsdownbot")
                        await com.delete()
                        if DUMP_GROUP:
                            await dump_file.copy(DUMP_GROUP)
                    except:
                        pass
            elif "stories" in url:
                meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
                if meta_tag.ok:
                    res = meta_tag.json()
                    meta = re.findall(r'href="(https?://[^"]+)"', res['data'])
                else:
                    return await message.reply("Oops something went wrong")
                try:
                    dump_file = await message.reply_video(meta[0], caption="Thank you for using - @InstaReelsdownbot")
                    if DUMP_GROUP:
                        await dump_file.copy(DUMP_GROUP)
                except:
                    com = await message.reply(meta[0])
                    await asyncio.sleep(1)
                    try:
                        dump_file = await message.reply_video(com.text, caption="Thank you for using - @InstaReelsdownbot")
                        await com.delete()
                        if DUMP_GROUP:
                            await dump_file.copy(DUMP_GROUP)
                    except:
                        pass
        except KeyError:
            await message.reply(f"400: Sorry, Unable To Find It Make Sure Its Publically Available :)")
        except Exception as e:
            if LOG_GROUP:
                await Mbot.send_message(LOG_GROUP, f"Instagram {e} {link}")
                await Mbot.send_message(LOG_GROUP, traceback.format_exc())
            await message.reply(f"400: Sorry, Unable To Find It  try another or report it  to @masterolic or support chat @spotify_supportbot 🤖")
    finally:
        await m.delete()
        if 'downfile' in locals():
            os.remove(downfile)
        await message.reply("Check out @spotify_downloa_bot(music)  @spotifynewss(Channel) \n Please Support Us By /donate To Maintain This Project")
