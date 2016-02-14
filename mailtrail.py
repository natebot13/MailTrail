from flask import Flask
import logging, sys
logging.basicConfig(stream=sys.stderr)

app = Flask(__name__)

import views
