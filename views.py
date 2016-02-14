"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import request, redirect, render_template
from mailtrail import app

import TextProcess
import json
import os

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='mailTrail',
        year=datetime.now().year,
    )

@app.route('/create')
def create():
    """Renders the about page."""
    return render_template(
        'create.html',
        title='Create',
        year=datetime.now().year,
        message='Create a game here!'
    )

# @app.route('/create/submit', methods=['POST', 'GET'])
# def create_submit():
#     passh

@app.route('/text', methods=['POST', 'GET'])
def text():
    print('Receiving text...')
    message = request.values.get('Body', None)
    person = request.values.get('From', None)
    jdata = {}
    if "textReg.json" in os.listDir():
        with open("textReg.json", "r") as jfile:
            jdata = json.load(jfile)

    if len(message.split()) > 1 and message.split()[0] == "switch":
        jdata[person] = message.split()[1]

    if person in jdata:
        gamename = jdata[person] + "@nathanp.me"
    else:
        gamename = 'treehacks@nathanp.me'
        jdata[person] = "treehacks"

    with open("textReg.json", "w") as jfile:
        json.dump(jdata, jfile)

    if not message or not person:
        return 'Incorrect POST data'
    TextProcess.evalAndRespond(person, message, gamename)
    return 'OK'



@app.route('/email', methods=['POST', 'GET'])
def email():
    print('Receiving email...')
    email = request.values.get('to', None)
    person = request.values.get('from', None)
    text = request.values.get('text', None)
    if not email or not person:
        return "Incorrect POST data"
    if not text:
        text = ""
    TextProcess.evalAndRespond(person, text, email)
    return 'OK'


@app.route('/text-test', methods=['GET', 'POST'])
def test():
    resp = twilio.twiml.Response()
    message = request.values.get('Body', None)
    if not message:
        return 'Incorect POST data'
    if 'hello' in message.lower():
        resp.message('world')
    return str(resp)
