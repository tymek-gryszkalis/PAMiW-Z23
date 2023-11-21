import dbController as db
import hashlib

def dbInit():
    db.init()

def registerUser(username, password):
    phash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    db.add("user", {"username" : username, "password" : phash})

def loginUser(username, password):
    u = db.select("user", "username", username)
    if u == []:
        return 2
    p = u[0][2]
    if hashlib.sha256(password.encode('utf-8')).hexdigest() == p:
        return 0
    else:
        return 1
    
def getUserID(username):
    u = db.select("user", "username", username)
    return int(u[0][0])

def validateUser(username):
    u = db.select("user", "username", username)
    if u == []:
        return False
    return True
    
def createSubject(curUser, subjectName):
    curUserID = getUserID(curUser)
    db.add("subject", {"userID" : curUserID, "name" : subjectName})

def getSubjectID(subjectName):
    s = db.select("subject", "name", subjectName)
    return int(s[0][0])

def getSubjectByID(subjectID):
    s = db.select("subject", "ID", subjectID)
    return s[0][2]

def getAllSubjects(curUser):
    u = getUserID(curUser)
    return db.select("subject", "userID", u)

def addNote(curUser, curSubject, title, data):
    u = getUserID(curUser)
    s = getSubjectID(curSubject)
    db.add("note", {"userID" : u, "subjectID" : s, "title" : title, "data" : data})

def getNotes(curUser):
    u = getUserID(curUser)
    return db.select("note", "userID", u)

def addFlashcardSet(curUser, curSubject, title):
    u = getUserID(curUser)
    s = getSubjectID(curSubject)
    db.add("flashSet", {"userID" : u, "subjectID" : s, "title" : title})

def getFlashSetID(flashTitle):
    f = db.select("flashSet", "title", flashTitle)
    return int(f[0][0])

def getAllFlashSets(curUser):
    u = getUserID(curUser)
    return db.select("flashSet", "userID", u)

def addFlashCard(flashSet, front, back):
    f = getFlashSetID(flashSet)
    db.add("flashcard", {"setID" : f, "front" : front, "back" : back})

def getFlashCards(flashTitle):
    f = getFlashSetID(flashTitle)
    return db.select("flashcard", "setID", f)

def removeNote(id):
    try:
        db.deleteByID("note", id)
    except:
        raise Exception
    
def removeFlashcard(id):
    try:
        db.deleteByID("flashcard", id)
    except:
        raise Exception
    
def removeFlashSet(id):
    try:
        db.deleteByID("flashset", id)
    except:
        raise Exception