"""
This script runs the FlaskWebProject application using a development server.
"""
import os
from os import environ
from FlaskWebProject import app
import sys
sys.path.insert(0, '/var/www/MailTrail')
os.chdir('/var/www/MailTrail')

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
