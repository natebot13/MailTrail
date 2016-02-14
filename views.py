"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import request, redirect, render_template
from mailtrail import app

import TextProcess

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
    print('Receiving text...')
    message = request.values.get('Body', None)
    person = request.values.get('From', None)
    gamename = 'treehacks@blank.b'
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
    if not gamename or not person or not text:
        return "Incorrect POST data"
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
