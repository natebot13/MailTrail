import Gameplay

import twilio.twiml
from twilio.rest import TwilioRestClient

import sendgrid

import os

account_sid = "AC3930798939ffc71eddac1cf3e515a462"
auth_token = "6a08e5998c52b12de9b4b36728ff2ad8"
client = TwilioRestClient(account_sid, auth_token)

sg = sendgrid.SendGridClient('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')

email_url = '@mailtrailgame.com'

def evalAndRespond(email, text, gamename):
	try:
		game = Gameplay.Game(gamename)
	except:
		msg = ""
		dirs = os.listdir("games/")
		for d in dirs:
			msg += d + "\n"
		sendMessage("adsf","asdf",msg,email)
		#sendTutorial(email)
		return
	if not email in game.subscribers:
		game.subscribe(email)
		sendWelcome(email,game)
		return

	segment = game.currentSegment(email)
	success, message = checkQuest(email, segment, text.split()[0])
	if not success:
		sendMessage(game.gamename, segment.title, segment.errorMessage + "\n\n" + bodyOfSegment(email, segment, game) + "\n\n" + tutorialText(), email)
	elif game.collaborative:
		scores = {}
		completedScores = {}
		for q in segment.quests:
			if q.participants[0] in scores:
				scores[q.participants[0]] += q.points
			else:
				scores[q.participants[0]] = q.points
		if segment.comleted:
			while segment.prizes and scores:
				winner = max(scores, key=(lambda k : scores[k]))
				completedScores.append(winner, segment.globalPrize + segment.prizes.pop())
				scores.pop(winner)

		for p in game.subscribers:
			endstr = ""
			if p in completedScores:
				endstr = completedScores[p]
			elif segment.completed:
				endstr = segment.globalPrize + segment.participationPrize

			if p == email:
				sendMessage(game.gamename, segment.title, "You completed a quest!\n\n" + bodyOfSegment(p, segment, game)+"\n\n"+ endstr,p)
			else:
				sendMessage(game.gamename, segment.title, "A quest was completed.\n\n" + bodyOfSegment(p, segment, game)+ "\n\n"+ endstr,p)

	else:
		sendMessage(game.gamename, segment.title, "You completed a quest!\n\n" + bodyOfSegment(p, segment, game) + "\n" + message, p)

def sendWelcome(email, game):
	sendMessage(game.gamename, "Welcome to " + game.gamename, game.description + "\n\n" + tutorialText(), email)

def sendTutorial(email):
	sendMessage("welcome","Welcome to MailTrail" ,"Welcome to MailTrail!\n\nTo get started, send an email to <gamename>@mailtrailgame.com where <gamename> is the name of the game you want to join.\n\n" + tutorialText(), email)

def tutorialText():
	return "How to play:\n1. Recieve emails with a list of quests to complete\n2. Follow the instructions for a quest to find the secret code\n3. Reply to the email with the code to complete the quest\n\nIt's as easy as that!  You can work competitively or collaboratively and there may be prizes such as gift cards involved!"

def bodyOfSegment(participant, segment, game):
	outstr = segment.description + "\nRequiredScore: " + segment.completionScore + "\n\n"
	for q in segment.quests:
		if (game.collaborative and q.participants) or (not game.collaborative and participant in q.participants):
			outstr += " x "
		else:
			outstr += " - "
		outstr += q.title + "\t" + q.points + "\n      " + q.description + "\n"
	outstr += "\n(Completed quests are marked with an 'x' while uncompleted quests are marked with a '-'.)\n"
	return outstr


def sendMessage(gamename,subject,body, to):
	if not "@" in to:
		#this must be a phone number so use text instead
		message = client.messages.create(to=to, from_="16195866665", body=body)
	else:
		message = sendgrid.Mail()
		message.add_to(to)
		message.set_subject(subject)
		message.set_text(body)
		message.set_from(gamename + email_url)
		status, msg = sg.send(message)
