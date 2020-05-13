from flask import request
import requests

from logs.printLog import printLog

'''
    Retrieves text from view-only Google docs
    Input: URL of google doc
    Output: text of google doc
'''
def acquireGoogle(url):
    printLog("URL is " + url)
    r = requests.get(url)
    content = r.text
    intel = processGoogleIntel(content)

    return intel

def processGoogleIntel(content):
    splitIntel = content.split('DOCS_modelChunk = [')

    intel = ''

    for chunk in splitIntel:
        bracketIndex = chunk.find('}')
        sIndex = chunk.find('s":"')
        chunk = chunk[sIndex + 4:bracketIndex]
        intel += chunk

    parsedIntel = intel.replace('\\n', '<br />')
    parsedIntel = parsedIntel.replace('\\t', '&emsp;')

    return parsedIntel