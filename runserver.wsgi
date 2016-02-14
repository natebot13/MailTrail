"""
This script runs the FlaskWebProject application using a development server.
"""
import sys
sys.path.insert(0, '/var/www/MailTrail')

from views import app as application
