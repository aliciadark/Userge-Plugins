# module by @yusukesy | tg @NoteZV
# kanged by Alicia dark | tg @eightbituwu

import json
import os
import time

import requests
from pytube import YouTube
from youtubesearchpython import Search, SearchVideos

from userge import Message, userge


def search_music(query):
    search = Search(query, limit=1)
    return search.result()["result"]


def search_video(query):
    search = SearchVideos(query, offset=1, mode="json", max_results=1)
    print(str(search.result()))
    return json.loads(search.result())["search_result"]


def get_link(result) -> str:
    return result[0]["link"]


def get_filename(result) -> str:
    title_ = str(result[0]["title"]).replace("/", "")
    title = title_.replace(" ", "_")
    return title + ".mp3", title + ".mp4"


def get_duration(result):
    duration = result[0]["duration"]
    secmul, dur, dur_arr = 1, 0, duration.split(":")
    for i in range(len(dur_arr) - 1, -1, -1):
        dur += int(dur_arr[i]) * secmul
        secmul *= 60
    return duration, dur


def get_thumb(result):
    thumbnail = result[0]["thumbnails"][0]["url"]
    title = str(result[0]["title"]).replace("/", "")
    thumb_name = f"{title}.jpg"
    thumb = requests.get(thumbnail, allow_redirects=True)
    open(os.path.join("./userge/xcache/", thumb_name), "wb").write(thumb.content)
    return thumb_name


def down_song(link, filename):
    YouTube(link).streams.filter(only_audio=True)[0].download(
        "./userge/xcache/", filename=filename
    )


def down_video(link, filename):
    YouTube(link).streams.get_highest_resolution().download(
        "./userge/xcache/", filename=filename
    )


@userge.on_cmd(
    "song",
    about={
        "header": "Music Downloader",
        "description": "Download music using pytube.",
        "usage": "{tr}song [name - artist / reply msg / link]",
    },
)
async def song(message: Message):
    music = message.input_or_reply_str
    if not music:
        await message.edit("`am i supposed to air swing it?!`")
        time.sleep(2)
        await message.delete()
        return
    await message.edit("`Processing...`")
    result = search_music(music)
    if result is None:
        await message.edit("`could not find the song.`")
        time.sleep(2)
        await message.delete()
        return
    link = get_link(result)
    duration, dur = get_duration(result)
    filename, m = get_filename(result)
    thumb = get_thumb(result)
    try:
        down_song(link, filename)
    except Exception as e:
        await message.edit("`unable to download the música.`")
        print(str(e))
        time.sleep(2)
        await message.delete()
    else:
        if os.path.exists(f"./userge/xcache/{thumb}"):
            caption = f"""
Title: __[{result[0]['title']}]({link})__
Duration: __{duration}__
Views: __{result[0]['viewCount']["text"]}__
"""
            try:
                await message.reply_audio(
                    audio=f"./userge/xcache/{filename}",
                    caption=caption,
                    title=result[0]["title"],
                    thumb=f"./userge/xcache/{thumb}",
                    duration=dur,
                )
            except Exception as e:
                await message.edit("`Unable to send the song.`")
                print(str(e))
                time.sleep(2)
                await message.delete()
            finally:
                await message.delete()
                os.remove(f"./userge/xcache/{filename}")
                os.remove(f"./userge/xcache/{thumb}")


@userge.on_cmd(
    "video",
    about={
        "header": "Video Downloader",
        "description": "Download videos using pytube. ;-;",
        "usage": "{tr}video [name / reply msg / link]",
    },
)
async def video(message: Message):
    video = message.input_or_reply_str
    if not video:
        await message.edit("`am i supposed to air swing it?!`")
        time.sleep(2)
        await message.delete()
        return
    await message.edit("`Processing...`")
    result = search_video(video)
    if result is None:
        await message.edit("`Unable to send the video.`")
        time.sleep(2)
        await message.delete()
        return
    link = get_link(result)
    m, filename = get_filename(result)
    try:
        down_video(link, filename)
    except Exception as e:
        await message.edit("`unable to download the video.`")
        time.sleep(2)
        await message.delete()
        print(str(e))
    else:
        caption = f"**Title ➠** __[{result[0]['title']}]({link})__\n**Channel ➠** __{result[0]['channel']}__"
        try:
            await message.reply_video(
                video=f"./userge/xcache/{filename}",
                caption=caption,
            )
        except Exception as e:
            await message.reply("`Unable to upload the video.`")
            print(str(e))
            time.sleep(2)
            await message.delete()
        finally:
            await message.delete()
            os.remove(f"./userge/xcache/{filename}")
