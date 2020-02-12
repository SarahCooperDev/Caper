from flask import request
import requests


def acquireFFnet(url):
    content = performRetrieval(url)
    intel = processIntel(content)
    
    if intel == -1:
        return -1
    else:
        furtherIntel = content
        newURL = url
        latestURL = url
        while furtherIntel != -1 or newURL != -1:
            newURL = getIntelLocation(newURL, furtherIntel)

            if newURL != -1:
                latestURL = newURL
                furtherIntel = performRetrieval(newURL)
                processedIntel = processIntel(furtherIntel)
                if processedIntel == -1:
                    break
                else:
                    intel += processedIntel
            else:
                break
        
        intel += '<p><a href="' + latestURL + '">' + latestURL + '</a></p>'
        return intel

def getIntelLocation(url, intel):
    intel = intel.split("<div class='storytext xcontrast_txt nocopy' id='storytext'>")
    intel = intel[1]
    intel = intel.split("<script>")
    intel = intel[0]

    if ">Next &gt;</button>" not in intel:
        return -1
    else:
        urlSplit = url.split('/')
        chapterCount = urlSplit[5]
        newCount = int(chapterCount) + 1
        print(chapterCount)

        newURL = ''
        for u in urlSplit:
            if u == chapterCount:
                newURL += str(newCount) + '/'
            else:
                newURL += str(u) + '/'

        return newURL 


def performRetrieval(url):
    print("URL is " + str(url))
    r = requests.get(url)
    content = r.text
    return content

def processIntel(content):
    print(content)
    intel = content.split("<div class='storytext xcontrast_txt nocopy' id='storytext'>")
    
    if len(intel) == 0:
        return -1
    else:
        intel = intel[1]
        intel = intel.split("</div>")
        intel = intel[0]
        
        return intel