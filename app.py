from flask import Flask, flash
from flask import render_template
from flask import request
from flask import redirect, url_for
import os

from models.restore_song_loot import updateLootProps, getLootProps, categoriseLoot
from models.joint_youtube import acquireYoutube
from models.mark_google import acquireGoogle
from models.mark_ffnet import acquireFFnet
from models.mark_smbc import acquireSmbc

app = Flask(__name__)
app.secret_key = b'speakthyvow'

###########################################################################
#                            Navigation                                   #
###########################################################################

@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('looting'), code=307)

@app.route('/looting', methods=['GET', 'POST'])
def looting():
    loot = bask()
    return render_template('looting.html', loot=loot)

@app.route('/discovery', methods=['GET', 'POST'])
def discovery():
    print("Discovery")
    if request.method == 'POST':
        intel = discoverIntel()
        return render_template('discovery.html', intel=intel)
    elif request.method == 'GET':
        return render_template('discovery.html')


###########################################################################
#                           Controllers                                   #
###########################################################################

# Call for altering the details of a piece of treasure
@app.route('/restore_loot', methods=['POST'])
def restoration():
    print("Restoring...")
    completed = restoreLoot()
    return redirect(url_for('looting'), code=307)

# Call for retrieving a piece of loot
@app.route('/execute_heist', methods=['POST'])
def executeHeist():
    print("Executing heist")
    response = acquireSong()
    categoriseLoot(response)
    flash(response)
    return redirect(url_for('looting'), code=307)


###################################################################
#                            API's                                #
###################################################################

@app.route('/api/discover_intel', methods=['POST'])
def discoverIntel():
    print("Discovering intel")
    if request.method == 'POST':
        target = request.form['target']
        acquisition = routeDiscovery(target)
        return acquisition

def routeDiscovery(target):
    acquisition = ''

    if 'docs.google.com' in target:
        acquisition = acquireGoogle(target)
    elif 'www.fanfiction.net' in target:
        acquisition = acquireFFnet(target)
    elif 'smbc-comics.com' in target:
        acquisition = acquireSmbc(target)
    else:
        print("Mark's security too high: level up to perform caper on " + str(target))

    return acquisition

@app.route('/api/restore_loot', methods=['POST'])
def restoreLoot():
    print('restoration')
    if request.method == 'POST':
        updateLootProps(request.form)

    return None

@app.route('/api/bask', methods=['GET'])
def bask():
    loot = getLootProps()
    return loot

@app.route('/api/acquire_song', methods=['POST'])
def acquireSong():
    print("Acquiring song")
    if request.method == 'POST':
        target = request.form['target']
        acquisition = acquireYoutube(target)
        print("Acquisition: " + acquisition)
        return acquisition

if __name__ == '__main__':
    app.run(debug=True)




#@app.route('/new_heist', methods=['GET'])
#def newHeist():
#    return redirect(url_for('looting'), code=307)

#@app.route('/mission_complete', methods=['POST'])
#def missionComplete():
#    print("Mission Complete!")
#    response = acquireSong()
#    print(response)
#    loot = bask()
#    return render_template('targetAquired.html', acquisition=response, loot=loot)