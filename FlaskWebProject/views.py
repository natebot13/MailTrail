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

@app.route('/receive-text', methods=['POST', 'GET'])
def text():
    resp = twilio.twiml.Response()
    message = request.values.get('Body', None)
    person = request.values.get('From', None)
    if not message or not person:
        return None
    message = message.split()
    g = Gameplay.Game(message[0])
    if g.checkQuest(person, message[1], "".join(message)):
        pass#TODO: resp.message(g.getSuccessMessage(message[1]))
    
    return str(resp)

@app.route('/text-test', methods=['GET', 'POST'])
def test():
    resp = twilio.twiml.Response()
    message = request.values.get('Body', None)
    if not message:
        return None
    if 'hello' in message.lower():
        resp.message('world')
    return str(resp)
