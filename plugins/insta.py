from pyrogram import filters, Client as Mbot
import bs4, requests, re, asyncio
import os, traceback, random
from bot import LOG_GROUP, DUMP_GROUP

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    #     "Accept-Encoding": "gzip, deflate, br",
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
        url = link.replace("instagram.com", "ddinstagram.com")
        url = url.replace("==", "%3D%3D")
        try:
            if url.endswith("="):
                dump_file = await message.reply_video(url[:-1], caption="Thank you for using - @InstaReelsdownbot")
            else:
                dump_file = await message.reply_video(url, caption="Thank you for using - @InstaReelsdownbot")
            return  # Prevent further execution
        except Exception as e:
            print(f"Error downloading from ddinsta: {e}")

        if "/reel/" in url:
            try:
                getdata = requests.get(url).text
                soup = bs4.BeautifulSoup(getdata, 'html.parser')
                meta_tag = soup.find('meta', attrs={'property': 'og:video'})
                if meta_tag:
                    content_value = f"https://ddinstagram.com{meta_tag['content']}"
                    dump_file = await message.reply_video(content_value, caption="Thank you for using - @InstaReelsdownbot")
                    return  # Prevent further execution
            except Exception as e:
                print(f"Error downloading from ddinsta (2): {e}")

        # If previous attempts failed, use saveig.app
        meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
        if meta_tag.ok:
            res = meta_tag.json()
            meta = re.findall(r'href="(https?://[^"]+)"', res['data'])
            if meta:
                if "/p/" in url or "stories" in url:
                    # Handle multiple media in posts and stories
                    for media_url in meta:
                        try:
                            dump_file = await message.reply_video(media_url, caption="Thank you for using - @InstaReelsdownbot")
                        except Exception as e:
                            print(f"Error sending media: {e}")
                else:
                    # Handle single media (reels)
                    try:
                        dump_file = await message.reply_video(meta[0], caption="Thank you for using - @InstaReelsdownbot")
                    except Exception as e:
                        print(f"Error sending media: {e}")
                return  # Prevent further execution
            else:
                await message.reply("No media found.")
        else:
            await message.reply("oops something went wrong with saveig.app")

    except KeyError:
        await message.reply(f"400: Sorry, Unable To Find It Make Sure Its Publically Available :)")
    except Exception as e:
        if LOG_GROUP:
            await Mbot.send_message(LOG_GROUP, f"Instagram {e} {link}")
            await Mbot.send_message(LOG_GROUP, traceback.format_exc())
        await message.reply(f"400: Sorry, Unable To Find It try another or report it to @masterolic or support chat @spotify_supportbot 🤖 ")
    finally:
        if 'dump_file' in locals():
            if DUMP_GROUP:
                await dump_file.copy(DUMP_GROUP)
        await m.delete()
        await message.reply("Check out @spotify_downloa_bot(music)  @spotifynewss(Channel) \n Please Support Us By /donate To Maintain This Project")
