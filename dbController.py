import sqlite3
import os

DBFILE = "database/database.db"

def init():
    try:
        os.remove(DBFILE)
    except Exception as e:
        print(e)
        pass
    con = sqlite3.connect(DBFILE)
    c = con.cursor()

    c.execute('''CREATE TABLE user (
              ID INTEGER PRIMARY KEY,
              username VARCHAR,
              password VARCHAR
        );
    ''')

    c.execute('''CREATE TABLE subject (
              ID INTEGER PRIMARY KEY,
              userID INTEGER,
              name VARCHAR,
              FOREIGN KEY(userID) REFERENCES user(ID)
        );
    ''')

    c.execute('''CREATE TABLE note (
              ID INTEGER PRIMARY KEY,
              userID INTEGER,
              subjectID INTEGER,
              title VARCHAR,
              data VARCHAR,
              FOREIGN KEY(subjectID) REFERENCES subject(ID),
              FOREIGN KEY(userID) REFERENCES user(ID)
        );
    ''')

    c.execute('''CREATE TABLE flashcard (
              ID INTEGER PRIMARY KEY,
              setID INTEGER,
              front VARCHAR,
              back VARCHAR,
              FOREIGN KEY(setID) REFERENCES flashSet(ID) 
        );
    ''')

    c.execute('''CREATE TABLE flashSet (
              ID INTEGER PRIMARY KEY,
              userID INTEGER,
              subjectID INTEGER,
              title VARCHAR,
              FOREIGN KEY(subjectID) REFERENCES subject(ID),
              FOREIGN KEY(userID) REFERENCES user(ID)
        );
    ''')

def add(table, content):
    con = sqlite3.connect(DBFILE)
    c = con.cursor()
    atrs = str(list(content.keys()))[1:-1].replace("\'", "")
    vals = str(list(content.values()))[1:-1]
    c.execute("INSERT INTO " + table + " (" + atrs + ") VALUES (" + vals + ")")
    con.commit()
    con.close()

def selectAll(table):
    con = sqlite3.connect(DBFILE)
    c = con.cursor()
    res = c.execute("SELECT * FROM " + table).fetchall()
    con.commit()
    con.close()
    return res

def select(table, patt, resp):
    con = sqlite3.connect(DBFILE)
    c = con.cursor()
    res = c.execute("SELECT * FROM " + table + " WHERE " + str(patt) + " = \'" + str(resp) + "\'").fetchall()
    con.commit()
    con.close()
    return res

def deleteByID(table, id):
    con = sqlite3.connect(DBFILE)
    c = con.cursor()
    c.execute("DELETE FROM " + table + " WHERE ID = " + str(id))
    con.commit()
    con.close()