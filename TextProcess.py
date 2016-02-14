import Gameplay

import twilio.twiml
from twilio.rest import TwilioRestClient

import sendgrid

account_sid = "AC3930798939ffc71eddac1cf3e515a462"
auth_token = "6a08e5998c52b12de9b4b36728ff2ad8"
client = TwilioRestClient(account_sid, auth_token)

sg = sendgrid.SendGridClient('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')

email_url = '@mailtrailgame.com'

def evalAndRespond(email, text, gamename):
    print(email,text,gamename)
