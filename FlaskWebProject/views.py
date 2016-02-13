"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import request, redirect, render_template
from FlaskWebProject import app

import twilio.twiml
from twilio.rest import TwilioRestClient

import Gameplay

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/text', methods=['POST', 'GET'])
def text():
    resp = twilio.twiml.Response()
    message = request.values.get('Body', None)
    person = request.values.get('From', None)
    if not message or not person:
        return None
    message = message.split()
    if len(message) < 3:
        return None
    g = Gameplay.Game(message[0])
    seg = g.currentStatus()
    if g.checkQuest(person, message[1], "".join(message[2:])):
        pass#TODO: resp.message(g.getSuccessMessage(message[1]))

    return str(resp)

@app.route('email', methods=['POST'])
def email():
    gamename = request.values.get('subject', None)
    if not gamename: return
    from_ = request.values.get('from', None)
    if not from_: return
    text = request.values.get('text', None)
    if not text: return
    g = Gameplay.Game(gamename)
    seg = 

@app.route('/text-test', methods=['GET', 'POST'])
def test():
    resp = twilio.twiml.Response()
    message = request.values.get('Body', None)
    if not message:
        return None
    if 'hello' in message.lower():
        resp.message('world')
    return str(resp)
