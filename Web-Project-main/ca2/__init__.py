from flask import Flask, session, request, redirect, flash, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user, logout_user
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta
from flask_limiter.util import get_remote_address
import secrets

auth = Blueprint('auth', __name__)

db = SQLAlchemy()
DB_NAME = "database.db"
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)


def create_app():
    app = Flask(__name__)
    
    # Configure Security Features
    app.config['SECRET_KEY'] = secrets.token_hex(32) # Secret key generation for the protection of cookies
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # Prevent SQL Injection
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20) # Permanent Session set to 20mins
    app.config['FAILED_LOGIN_ATTEMPTS'] = 3  # Maximum failed login attempts
    app.config['ACCOUNT_LOCKOUT_DURATION'] = 5  # Lockout duration in minutes
    
    
    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
# To check crsf token generation
#    @app.before_request
#    def log_request():
#        print(request.form.get('csrf_token'))

    @app.before_request
    def before_request():
        session.permanent = True
        exempt_routes = ['auth.login', 'static']  # Add 'static' to avoid issues with static files
        if request.endpoint in exempt_routes:
            return

        if current_user.is_authenticated:
            last_activity = session.get('last_activity')
            if not last_activity or datetime.utcnow().timestamp() - last_activity > 120:  # 2 minutes
                logout_user()
                session.clear()
                flash('Session expired. Please login again.', category='error')
                redirect(url_for('auth.login'))
        session['last_activity'] = datetime.utcnow().timestamp()
        
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
