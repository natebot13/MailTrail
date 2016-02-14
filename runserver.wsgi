"""
This script runs the FlaskWebProject application using a development server.
"""
import logging, sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/MailTrail')

from mailtrail import app as application
