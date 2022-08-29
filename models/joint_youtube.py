from flask import request
import youtube_dl
import os

from logs.printLog import printLog

currentPath = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
lootFolder = os.path.join(currentPath, 'loot')

def acquireYoutube(url):
    printLog("In devour dl")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(lootFolder, '%(title)s' + '.%(ext)s'),
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        printLog(info)
        printLog(info.get('title'))
        title = info.get('title')
        titleDecoded = title.encode("ascii", errors="ignore").decode().replace('||', '')
        titleDecoded = titleDecoded.encode("ascii", errors="ignore").decode().replace('"', '')
        titleDecoded = titleDecoded.encode("ascii", errors="ignore").decode().replace('\'', '')
        printLog("done")
        printLog(titleDecoded)
        os.rename(os.path.join(lootFolder, title.replace('||', '_').replace('"', '\'') + '.mp3'), os.path.join(lootFolder, titleDecoded + '.mp3'))
        return titleDecoded
