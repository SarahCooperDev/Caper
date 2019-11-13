from flask import Flask, flash
from flask import render_template
from flask import request
from flask import redirect, url_for
import os

from models.restoration import updateLootProps, getLootProps, categoriseLoot
from models.joint_youtube import acquireYoutube

app = Flask(__name__)
app.secret_key = b'speakthyvow'

@app.route('/', methods=['GET', 'POST'])
def home():
    loot = bask()
    return render_template('thePlan.html', loot=loot)

@app.route('/new_heist', methods=['GET'])
def newHeist():
    return redirect(url_for('home'), code=307)

@app.route('/restore_loot', methods=['POST'])
def restoration():
    print("Restoring...")
    completed = restoreLoot()
    return redirect(url_for('home'), code=307)

@app.route('/execute_heist', methods=['POST'])
def executeHeist():
    print("Execute")
    response = acquireSong()
    categoriseLoot(response)
    flash(response)
    return redirect(url_for('home'), code=307)

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

@app.route('/mission_complete', methods=['POST'])
def missionComplete():
    print("Mission Complete!")
    response = acquireSong()
    print(response)
    loot = bask()
    return render_template('targetAquired.html', acquisition=response, loot=loot)

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
