from flask import Flask, flash
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import send_file
import os

from models.restore_song_loot import updateLootProps, getLootProps, categoriseLoot
from models.joint_youtube import acquireYoutube
from models.mark_google import acquireGoogle
from models.mark_ffnet import acquireFFnet
from models.mark_smbc import acquireSmbc

from logs.printLog import printLog

app = Flask(__name__)
app.secret_key = b'judgemyvow'

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
    printLog("Restoring...")
    completed = restoreLoot()
    return redirect(url_for('looting'), code=307)

# Call for retrieving a piece of loot
@app.route('/execute_heist', methods=['POST'])
def executeHeist():
    printLog("Executing heist")
    response = acquireSong()
    categoriseLoot(response)
    flash(response)
    return redirect(url_for('looting'), code=307)


###################################################################
#                            API's                                #
###################################################################

@app.route('/store_loot')
def storeLoot():
    filename = request.args.get('filename')
    printLog('filename ' + str(filename))
    return send_file('../loot/' + filename, mimetype='audio/mpeg', attachment_filename=filename, as_attachment=True)


@app.route('/api/discover_intel', methods=['POST'])
def discoverIntel():
    printLog("Discovering intel")
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
        printLog("Mark's security too high: level up to perform caper on " + str(target))

    return acquisition

@app.route('/api/restore_loot', methods=['POST'])
def restoreLoot():
    printLog('restoration')
    if request.method == 'POST':
        updateLootProps(request.form)

    return None

@app.route('/api/bask', methods=['GET'])
def bask():
    loot = getLootProps()
    return loot

@app.route('/api/acquire_song', methods=['POST'])
def acquireSong():
    printLog("Acquiring song")
    if request.method == 'POST':
        target = request.form['target']
        acquisition = acquireYoutube(target)
        printLog("Acquisition: " + acquisition)
        return acquisition

if __name__ == '__main__':
    app.run(debug=True, port=80)