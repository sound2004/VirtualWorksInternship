from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256
from . import db   # means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta
from markupsafe import escape
import re

auth = Blueprint('auth', __name__)
limiter = Limiter(key_func=get_remote_address) # Prevention of DoS attacks by limiting requests per client

# Condition for account lockout
login_attempt_max = 3
locked_duration = timedelta(minutes=5)


# Check if Password is Valid
def is_password_valid(password):
    return (len(password) >= 8 and 
            any(c.isupper() for c in password) and 
            any(c.islower() for c in password) and 
            any(c.isdigit() for c in password) and 
            any(not c.isalnum() for c in password))

# Check if email is meets requirment using regrex
email_checker = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Data Input Sanitization
def check_input(text):
    return escape(text.strip())

def check_account_locked(user):
    if user.locked_until and user.locked_until > datetime.utcnow():
        return True
    return False


@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit("5/minute")
def login():
    if request.method == 'POST':
        email = check_input(request.form.get('email', ''))
        password = check_input(request.form.get('password', ''))

        user = User.query.filter_by(email=email).first()
        if user:
            # Check the lock status of the account
            if check_account_locked(user):
                remaining_time = user.locked_until - datetime.utcnow()
                flash(f'Your Account is locked. Try again in {int(remaining_time.total_seconds() / 60)} minutes.', category='error')
                return render_template("login.html", user=current_user)

            # Using a stronger Password algorimth
            if pbkdf2_sha256.verify(password, user.password):
                user.failed_login_attempts = 0
                user.locked_until = None
                db.session.commit()
                login_user(user, remember=True)
                session.permanent = True
                session['user_id'] = user.id
                session['last_activity'] = datetime.utcnow().timestamp()
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                # Increment failed attempts
                user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
                if user.failed_login_attempts >= login_attempt_max:
                    user.locked_until = datetime.utcnow() + locked_duration
                    flash(f'Your Account is locked for {locked_duration.seconds // 60} minutes due to 3 failed attempts.', category='error')
                else:
                    remaining_attempts = login_attempt_max - user.failed_login_attempts
                    flash(f'Incorrect password, Please Try Again. {remaining_attempts} attempts remaining.', category='error')
                db.session.commit()
        else:
            flash('Email does not exist.', category='error')   
                
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    session.clear() # On Logout clear all session
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = check_input(request.form.get('email', ''))
        first_name = check_input(request.form.get('firstName', ''))
        surname= check_input(request.form.get('surname', ''))
        password1 = check_input(request.form.get('password1', ''))
        password2 = check_input(request.form.get('password2', ''))

        # Fulfil email and improved password requirment
        if not email_checker.match(email):
            flash('Please enter a valid email address.', category='error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be at least 2 characters.', category='error')
        elif len(surname) < 2:
            flash('Surname must be at least 2 characters.', category='error')
        elif password1 != password2:
            flash('Password do not match.', category='error')    
        elif not is_password_valid(password1):
            flash('Password must be at least 8 characters and contain uppercase, lowercase, numbers, and symbols.', category='error')
        else:
            hashed_password = pbkdf2_sha256.hash(password1)
            new_user = User(email=email, first_name=first_name, surname=surname, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            session.permanent = True
            session['user_id'] = new_user.id
            session['last_activity'] = datetime.utcnow().timestamp()
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user=current_user)
