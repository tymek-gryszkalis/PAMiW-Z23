from flask import Blueprint, render_template,flash, request, redirect, url_for
from .models import Note, Flashset, Flashcard
from flask_login import login_required, current_user
from . import db
from datetime import date

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    return render_template("home.html")

@views.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    if request.method == "POST":
        if request.form.get("action") == "addNote":
            title = "Untitled note" if request.form.get("title") == "" else request.form.get("title")
            content = request.form.get("content")
            note = Note(title = title, content = content, userId = current_user.id, createDate = date.today())
            db.session.add(note)
            db.session.commit()
            return redirect(url_for("views.notes"))
        if request.form.get("action") == "saveNote":
            note = Note.query.filter_by(id = request.form.get("noteId")).first()
            note.title = "Untitled note" if request.form.get("title") == "" else request.form.get("title")
            note.content = request.form.get("content")
            db.session.commit()
            return redirect(url_for("views.notes"))
        else:
            Note.query.filter_by(id = request.form.get("action")).delete()
            db.session.commit()
            return redirect(url_for("views.notes"))
    notes = Note.query.filter_by(userId = current_user.id)
    return render_template("notes.html", notes = notes)

@views.route("/flashsets", methods=["GET", "POST"])
@login_required
def flashsets():
    if request.method == "POST":
        if request.form.get("action") == "addFlashset":
            title = "Untitled set" if request.form.get("title") == "" else request.form.get("title")
            newFS = Flashset(title = title, userId = current_user.id, numOfCards = 0)
            db.session.add(newFS)
            db.session.commit()
        else:
            Flashset.query.filter_by(id = request.form.get("action")).delete()
            flashcardsToDelete = Flashcard.query.filter_by(flashsetId = request.form.get("action"))
            for f in flashcardsToDelete:
                Flashcard.query.filter_by(id = f.id).delete()
            db.session.commit()
        return redirect(url_for("views.flashsets"))
    flashsets = Flashset.query.filter_by(userId = current_user.id)
    return render_template("flashsets.html", flashsets = flashsets)

@views.route("/flashsets/<flashsetid>", methods=["GET", "POST"])
@login_required
def view_flashset(flashsetid):
    flashset = Flashset.query.filter_by(id = flashsetid).first()
    if request.method == "POST":
        if request.form.get("action") == "addFlashcard":
            front = request.form.get("front")
            back = request.form.get("back")
            newFlashCard = Flashcard(front = front, back = back, flashsetId = flashsetid)
            flashset.numOfCards += 1
            db.session.add(newFlashCard)
            db.session.commit()
        else:
            Flashcard.query.filter_by(id = request.form.get("action")).delete()
            flashset.numOfCards -= 1
            db.session.commit()
        return redirect(url_for("views.view_flashset", flashsetid = flashsetid))
    flashcards = Flashcard.query.filter_by(flashsetId = flashsetid)
    title = Flashset.query.filter_by(id = flashsetid).first().title
    return render_template("view_flashset.html", flashcards = flashcards, title = title)
