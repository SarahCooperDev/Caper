from flask import request
import eyed3
import os

def categoriseLoot(filename):
    audiofile = eyed3.load("../loot/" + filename  + '.mp3')
    audiofile.tag.title = filename
    audiofile.tag.artist = 'Unknown'
    audiofile.tag.album = 'Unknown'
    audiofile.tag.save()

    return 0

def updateLootProps(form):
    title = form['title']
    artist = form['artist']
    album = form['album']
    filename = form['filename']
    print('Title: ' + title)
    print('artist: ' + artist)
    print(' album: ' + album)
    print('filename: ' + filename)

    audiofile = eyed3.load("../loot/" + filename)
    audiofile.tag.title = title
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.save()

    return 0

def getLootProps():
    lootFiles = os.listdir('../loot')
    print(lootFiles)

    loot = []

    for lootprops in lootFiles:
        audiofile = eyed3.load("../loot/" + lootprops)
        print(audiofile)
        print(audiofile.tag.artist)
        print(audiofile.tag.album)
        print(audiofile.tag.title)
        loot.append({'filename': lootprops, 'title':audiofile.tag.title, 'artist': audiofile.tag.artist, 'album': audiofile.tag.album})

    return loot