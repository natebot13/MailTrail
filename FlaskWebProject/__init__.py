"""
The flask application package.
"""
import sys
sys.path.insert(0, '/var/www/MailTrail')

from flask import Flask
app = Flask(__name__)

import FlaskWebProject.views
