import Gameplay

import twilio.twiml
from twilio.rest import TwilioRestClient

from NotOnGit import account_sid, auth_token, sgk

import sendgrid

client = TwilioRestClient(account_sid, auth_token)

sg = sendgrid.SendGridClient(sgk)




email_url = '@mailtrailgame.com'

def evalAndRespond(email, text, gamemail):
	gamename = gamemail[:gamemail.find("@")]
	try:
		game = Gameplay.Game(gamename)
	except:
		sendTutorial(email)
		return
	game.gamemail = gamemail

	segment = game.currentSegment(email)

	if not segment:
		sendMessage(game.gamemail, game.gamename + " Completed", "The game '" + game.gamename + "' has already been comleted.  Congratulations!", email)
	if not email in game.subscribers:
		game.subscribe(email)
		sendWelcome(email,segment,game)
		return
	txt = text.split()[0] if text.split() else ""
	success = game.checkQuest(email, segment, txt)
	if not success:
		if txt == "what":
			sendMessage(game.gamemail, segment.title, segment.errorMessage + "\n\n" + bodyOfSegment(email, segment, game) + "\n\n" + tutorialText(), email)
		else:
			sendMessage(game.gamemail, segment.title, segment.errorMessage + "\n\n" + bodyOfSegment(email, segment, game), email)
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
				sendMessage(game.gamemail, segment.title, "You completed a quest!\n\n" + bodyOfSegment(p, segment, game)+"\n\n"+ endstr,p)
			else:
				sendMessage(game.gamemail, segment.title, "A quest was completed.\n\n" + bodyOfSegment(p, segment, game)+ "\n\n"+ endstr,p)

	else:
		message = ""
		if sum([q.points for q in segment.quests if email in q.participants]) >= segment.completionScore:
			if segment.globalPrize:
				message = segment.globalPrize + "\n"
			if segment.prizes:
				message += segment.prizes.pop() + "\n"
			elif segment.participationPrize:
				message += segment.participationPrize() + "\n"

		sendMessage(game.gamemail, segment.title, "You completed a quest!\n\n" + bodyOfSegment(email, segment, game) + "\n" + message, email)
	game.update()

def sendWelcome(email, segment, game):
	if "@" in email:
		sendMessage(game.gamemail, "Welcome to " + game.gamename, game.description + "\n\n" + bodyOfSegment(email,segment,game) +"\n\n"+ tutorialText() + "\n\nReply to this email to get started!", email)
	else:
		sendMessage(game.gamemail, "Welcome to " + game.gamename, '<p style="font-size:14px">' + game.description + '</p>' + "\n\n" + bodyOfSegment(email,segment,game) +"\n\n"+ '<p style="font-size:10px">' + tutorialText() + '</p>' + "\n\n<b>Reply to this email to get started!</b>", email)

def sendTutorial(email):
	sendMessage("welcome@mailtrailgame.com","Welcome to MailTrail" ,"Welcome to MailTrail!\n\nTo get started, send an email to <gamename>@mailtrailgame.com where <gamename> is the name of the game you want to join.\n\n" + tutorialText(), email)

def tutorialText():
	return "How to play:\n1. Recieve emails with a list of quests to complete\n2. Follow the instructions for a quest to find the secret code\n3. Reply to the email with the code to complete the quest\n\nIt's as easy as that!  You can work competitively or collaboratively and there may be prizes such as gift cards involved!"

def bodyOfSegment(participant, segment, game):
	if "@" in participant:
		outstr = '<p style="font-size:14px">' + segment.description + '<br><p style="font-size:13px"><i>RequiredScore: ' + str(segment.completionScore) + "</i></p>\n\n"
	else:
		outstr = segment.description + "\nRequiredScore: " + str(segment.completionScore) + "\n\n"
	for q in segment.quests:
		if "@" in participant:
			if (game.collaborative and q.participants) or (not game.collaborative and participant in q.participants):
				outstr += ' <p style="font-size:20px">&#x25A1</p> '
			else:
				outstr += ' <p style="font-size:20px">&#x2611FE0E</p> '
			outstr += "<b>[" + str(q.points) + "]</b> "
			outstr += q.title + "<br><p margin-left:10em><i>" + q.description + "</i></p><br>"
		else:
			if (game.collaborative and q.participants) or (not game.collaborative and participant in q.participants):
				outstr += " X "
			else:
				outstr += " - "
			outstr += "[" + str(q.points) + "] "
			outstr += q.title + "\n      " + q.description + "\n"
	if not "@" in participant:
		outstr += "\n(Completed quests are marked with an 'X' while uncompleted quests are marked with a '-'.)\n"
	return outstr


def sendMessage(gamemail, subject, body, to):
	if not "@" in to:
		#this must be a phone number so use text instead
		print('Sending reply to:', to)
		message = client.messages.create(to=to, from_="16195866665", body=body)
		print(message)
	else:
		message = sendgrid.Mail()
		message.add_to(to)
		message.set_subject(subject)
		message.set_html(body)
		message.set_from(gamemail)
		status, msg = sg.send(message)
