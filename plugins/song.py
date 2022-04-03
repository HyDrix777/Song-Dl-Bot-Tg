import os
import time
import ffmpeg
import logging
import requests
import youtube_dl
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


## Extra Fns -------
# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------
@Client.on_message(filters.command(['start']))
async def start(client, message):
       await message.reply("╭─────※🎶※────⍟\n│🧑‍💻 Hᴇʟʟᴏ\n│I'ᴍ ᴍᴜsɪᴄ ᴅʟʀ[📥](https://telegra.ph/file/afbcaeb494cd50fc0e568.jpg)\n│Exᴄʟᴜsɪᴠᴇʟʏ ᴍᴀᴅᴇ ғᴏʀ👇🏼\n├▶️ [Music Galaxy](https://t.me/Music_Galaxy_Dl)\n│Jᴏɪɴ ᴍʏ ɢʀᴏᴜᴘ & Sᴇᴇ ᴡʜᴀᴛ ᴄᴀɴ I ᴅᴏ🎶\n╰─────※🎶※────⍟",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('👥 Group', url='https://t.me/Music_Galaxy_Dl'),
                    InlineKeyboardButton('MG', url='https://t.me/Music_Galaxy_Dl')
                ],
                [
                    InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['help']))
async def help(client, message):
       await message.reply("<b>Simplest Way😂</b>\n\n<i>How many times have I said that just giving the name of a song is enough.🙄\nDo not expect any other help from me😠</i>\n\n<b>Eg :</b> `/s Vaathi Coming`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Music', url='https://t.me/Music_Galaxy_Dl')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['about']))
async def about(client, message):
       await message.reply("➥<b>Name</b> : ⍟<i>Music Downloader</i>\n➥<b>Group</b> : ⍟[Music Galaxy](https://t.me/Music_Galaxy_Dl)\n➥<b>Language</b> : ⍟<i>Python3</i>\n➥<b>Server</b> : ⍟[𝘏𝘦𝘳𝘰𝘬𝘶](https://heroku.com/)\n➥<b>Source</b> : ⍟[𝘊𝘭𝘪𝘤𝘬 𝘏𝘦𝘳𝘦](https://t.me/Music_Galaxy_Dl)",
       reply_markup=InlineKeyboardMarkup(
           [
               [
                   InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')
               ]
           ]
        )
    )

@Client.on_message(filters.command(['s']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🔎 𝗦𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴 𝘁𝗵𝗲 𝗦𝗼𝗻𝗴...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐓𝐫𝐲 𝐂𝐡𝐚𝐧𝐠𝐢𝐧𝐠 𝐓𝐡𝐞 𝐒𝐩𝐞𝐥𝐥𝐢𝐧𝐠 𝐀 𝐋𝐢𝐭𝐭𝐥𝐞 😐')
            return
    except Exception as e:
        m.edit(
            "❎ 𝐹𝑜𝑢𝑛𝑑 𝑁𝑜𝑡ℎ𝑖𝑛𝑔. 𝐒𝐨𝐫𝐫𝐲.\n\n𝖯𝗅𝖾𝖺𝗌𝖾 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 𝖮𝗋 𝖲𝖾𝖺𝗋𝖼𝗁 𝖺𝗍 Google.com 𝖥𝗈𝗋 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝗈𝖿 𝗍𝗁𝖾 𝙎𝙤𝙣𝙜.\n\nEg.`/s Believer`"
        )
        print(str(e))
        return
    m.edit("📤Uploading To Telegram")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep =  f'🎧 Title: [{title[:35]}]({link})\n⏳ Duration: `{duration}`\n👀 Views: `{views}`\n\n📮 By: {message.from_user.mention()}\n📤 By: @Music_Galaxy_Dl)'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=str(info_dict["uploader"]), thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('`Faild Try Again Later`')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
