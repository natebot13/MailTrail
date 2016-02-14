"""
This script runs the FlaskWebProject application using a development server.
"""
import sys
sys.path.insert(0, '/var/www/MailTrail')
from os import environ
from views import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
