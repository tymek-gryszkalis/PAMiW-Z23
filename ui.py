import logic

curUser = "admin"
loggedIn = True

while True:
    inp = input("> ").split(" ")

    if inp[0] == "init":
        logic.dbInit()
        print("Database initiated.")
        continue
    
    if inp[0] == "register":
        if logic.validateUser(inp[1]):
            print("Username " + inp[1] + " already registered")
            continue
        logic.registerUser(inp[1], inp[2])
        print("User " + inp[1] + "registered")
        continue

    if inp[0] == "login":
        r = logic.loginUser(inp[1], inp[2])
        if r == 0:
            curUser = inp[1]
            print("Login as " + inp[1] + " successful")
        elif r == 1:
            print("Wrong password")
        elif r == 2:
            print("User not found")
        continue
    
    if inp[0] == "whoami":
        if loggedIn:
            print(curUser)
        else:
            print("Not logged in")
        continue

    if inp[0] == "add":
        if inp[1] == "subject":
            name = input("Subject name: ")
            logic.createSubject(curUser, name)
            continue

        if inp[1] == "note":
            subs = []
            for i in logic.getAllSubjects(curUser):
                subs.append(i[2])
            subject = input("Choose subject (Availible: " + ", ".join(subs) + "): ")
            if subject not in subs:
                print("Subject doesn't exist")
                continue
            title = input("Title note: ")
            note = input("Write note: ")
            logic.addNote(curUser, subject, title, note)
            continue

        if inp[1] == "flashset":
            subs = []
            for i in logic.getAllSubjects(curUser):
                subs.append(i[2])
            subject = input("Choose subject (Availible: " + ", ".join(subs) + "): ")
            if subject not in subs:
                print("Subject doesn't exist")
                continue
            title = input("Title flashset: ")
            logic.addFlashcardSet(curUser, subject, title)
            continue

        if inp[1] == "flashcard":
            fss = []
            for i in logic.getAllFlashSets(curUser):
                fss.append(i[3])
            fs = input("Choose flashcard set (Availible: " + ", ".join(fss) + "): ")
            if fs not in fss:
                print("Flashcard set doesn't exist")
                continue
            front = input("Write front: ")
            back = input("Write back: ")
            logic.addFlashCard(fs, front, back)
            continue

    if inp[0] == "read":
        if inp[1] == "note":
            n = logic.getNotes(curUser)
            if n == []:
                print("No notes availible")
                continue
            for i in n:
                s = logic.getSubjectByID(i[2])
                print(str(i[0]) + ") " + s + " " + i[3] + " " + i[4])
            continue

        if inp[1] == "flashset":
            fss = []
            for i in logic.getAllFlashSets(curUser):
                fss.append(i[3])
            if fss == []:
                print("No flashcard sets availible")
                continue
            fs = input("Choose flashcard set (Availible: " + ", ".join(fss) + "): ")
            if fs not in fss:
                print("Flashcard set doesn't exist")
                continue
            res = logic.getFlashCards(fs)
            for i in res:
                print(str(i[0]) + ") f: " + i[2] + " b: " + i[3])
            continue
        
    if inp[0] == "remove":
        if inp[1] == "note":
            tr = input("Number of note to remove: ")
            try:
                logic.removeNote(tr)
            except:
                print("Cannot remove note")
            continue

        if inp[1] == "flashcard":
            fss = []
            for i in logic.getAllFlashSets(curUser):
                fss.append(i[3])
            fs = input("Choose flashcard set (Availible: " + ", ".join(fss) + "): ")
            if fs not in fss:
                print("Flashcard set doesn't exist")
                continue
            tr = input("Number of flashcard to remove: ")
            try:
                logic.removeFlashcard(tr)
            except:
                print("Cannot remove flashcard")
            continue

        if inp[1] == "flashset":
            fss = []
            for i in logic.getAllFlashSets(curUser):
                fss.append(i[3])
            fs = input("Choose flashcard set to delete (Availible: " + ", ".join(fss) + "): ")
            if fs not in fss:
                print("Flashcard set doesn't exist")
                continue
            fcs = logic.getFlashCards(fs)
            for i in fcs:
                logic.removeFlashcard(i[0])
            fid = logic.getFlashSetID(fs)
            logic.removeFlashSet(fid)
    print("Unknown command")