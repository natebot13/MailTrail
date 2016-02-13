import json
class Game:
    def __init__(self,gamename):
        self.gamename = gamename
        with open("games/" + gamename + ".json", "r") as jfile:
            jdata = json.load(jfile)
        if "creator" in jdata:
            self.creator = jdata["creator"]
        else:
            self.creator = ""
        if "subscribers" in jdata:
            self.subscribers = jdata["subscribers"]
        else:
            self.subscribers = []
        self.collaborative = jdata["collaborative"]
        self.title = jdata["title"]
        self.description = jdata["description"]
        self.segments = [Segment(d) for d in jdata["segments"]]
        self.didUpdate = False


    #returns the most current segment
    def currentStatus(self,participant):
        if self.collaborative:
            for seg in self.segments:
                if seg.status < seg.completionScore:
                    return seg
        else:
            for seg in self.segments:
                for quest in seg.quests:
                    if not participant in quest.participants:
                        return seg

    def setCreator(self,creator):
        self.creator = creator

    def subscribe(self,participant):
        if not participant in self.participants:
            sefl.participants.append(participant)

    def dictValue(self):
        rd = {"title" : self.title, "description" : self.description, "collaborative" : self.collaborative}
        if self.creator:
            rd["creator"] = self.creator
        if self.subscribers:
            rd["subscribers"] = self.participants
        rd["segments"] = [s.dictValue() for s in self.segments]
        return rd

    def update(self):
        with open("games/" + self.gamename + ".json", "w") as jfile:
            json.dump()
        self.didUpdate = True

    #validates a submitted code and updates stuff if it was valid
    def checkQuest(self,participant, quest, code):
        if quest.code == code:
            quest.participants.append(participant)
            if not participant in self.subscribers:
                self.subscribers.append(participant)
            self.update
            return True
        else:
            return False



class Segment:
    def __init__(self,d):
        self.title = d["title"]
        self.description = d["description"]
        self.completionScore = d["completionScore"]
        self.quests = [Quest(q) for q in d["quests"]]
        self.status = sum([q.points for q in self.quests if q.completed])

    def dictValue():
        rd = {"title" : self.title, "description" : self.description, "completionScore" : self.completionScore}
        rd["quests"] = [q.dictValue() for q in self.quests]
        return rd



class Quest:
    def __init__(self,q):
        self.title = q["title"]
        self.description = q["description"]
        self.code = q["code"]
        self.points = q["points"]
        if "participants" in q:
            self.participants = q["participants"]
            self.completed = True
        else:
            self.participants = []
            self.completed = False

    def dictValue():
        rd = {"title" : self.title, "description" : self.description, "code" : self.code, "points" : self.points}
        if self.participants:
            rd["participants"] = self.participants
        return rd
