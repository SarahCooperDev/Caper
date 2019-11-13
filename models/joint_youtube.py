from flask import request
import youtube_dl
import os

def acquireYoutube(url):
    print("In devour dl")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '../loot/' + '%(title)s' + '.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        print(info)
        print(info.get('title'))
        title = info.get('title')
        titleDecoded = title.encode("ascii", errors="ignore").decode().replace('||', '')
        print("done")
        print(titleDecoded)
        os.rename('../loot/' + title.replace('||', '_') + '.mp3', '../loot/' + titleDecoded + '.mp3')
        return titleDecoded