from flask import request
import requests

from logs.printLog import printLog

def acquireSmbc(url):
    count = 0
    intel = ''
    furtherIntel = ''
    newURL = url
    latestURL = url

    while furtherIntel != -1 and newURL != -1 and count <= 100:
        printLog("In while")
        furtherIntel = performRetrieval(newURL)
        processedIntel = processIntel(furtherIntel)

        if processedIntel == -1:
            break
        else:
            title = getTitle(processedIntel)
            processedIntel += '<p>' + str(title) + '</p>'
            aftercomic = getAfter(furtherIntel)
            processedIntel += aftercomic

            intel += processedIntel
            count += 1

            newURL = getIntelLocation(newURL, furtherIntel)

            if newURL != -1:
                latestURL = newURL
            else:
                break
    
    intel += '<p><a href="' + latestURL + '">' + latestURL + '</a></p>'
    intel += '<p>Total Stolen: ' + str(count) + '</p>'
    return intel

def getIntelLocation(url, intel):
    if '<a class="cc-next" rel="next" href="' not in intel:
        return -1
    else:
        navIndex = intel.split('<a class="cc-next" rel="next" href="')
        navElement = navIndex[1]
        closeNavIndex = navElement.index('"')
        nextLink = navElement[:closeNavIndex]
        printLog("New Link " + str(nextLink))

        return nextLink

def performRetrieval(url):
    printLog("URL is " + str(url))
    r = requests.get(url)
    content = r.text
    return content

def getTitle(content):
    titleDiv = content.split('<img title="')
    titleStart = titleDiv[1]
    title = titleStart.split('"')
    title = title[0]
    return title

def getAfter(content):
    afterDiv = content.split('<div id="aftercomic"')
    afterStart = afterDiv[1]
    afterImg = afterStart.split("<img src='")
    afterSrc = afterImg[1].split("'")
    after = '<img src="' + afterSrc[0] + '"><br/>'
    return after

def processIntel(content):
    intel = content.split('<div id="cc-comicbody">')
    intel = intel[1]
    intel = intel.split('<script>')
    intel = intel[0]
    
    if len(intel) == 0:
        return -1
    else:        
        return intel