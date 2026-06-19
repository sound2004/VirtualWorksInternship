from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .models import Note
from . import db
import json
from markupsafe import escape


views = Blueprint('views', __name__)
auth = Blueprint('auth', __name__)
limiter = Limiter(key_func=get_remote_address)

# Data Input Sanitization
def check_input(text):
    return escape(text.strip())

@views.route('/update-note', methods=['POST'])
@login_required
@limiter.limit("5/minute")
def update_note():
    try:
        note_data = json.loads(request.data)
        note_id = note_data.get('noteId')
        new_content = check_input(note_data.get('content', ''))
        
        note = Note.query.get(note_id)
        if note and note.user_id == current_user.id:
            if len(new_content) < 0:
                return jsonify({"error": "Please add a note!"}), 400
            note.data = new_content
            db.session.commit()
            flash('Your note updated successfully!', category='success')
            return jsonify({"success": True})
        return jsonify({"error": "Note not found or unauthorized"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@login_required
@limiter.limit("5/minute")
def home():
    if request.method == 'POST': 
        note = check_input(request.form.get('note', '')) # Gets the note from the HTML 

        if len(note) < 0:
            flash('Please add a Note!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Your note is added!', category='success')

    return render_template("home.html", user=current_user)




@views.route('/delete-note', methods=['POST'])
@login_required
@limiter.limit("5/minute")
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Your note is deleted!', category='success')

    return jsonify({})
