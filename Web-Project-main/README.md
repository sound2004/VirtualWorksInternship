# Flask Notes App

A secure web application built with Flask that allows users to create, store and delete notes. The application implements various security features including session management, account lockout, and protection against common web vulnerabilities (e.g., SQL injection prevention, secure session handling, input validation). The project will build upon an existing GitHub open source-code created by GitHub User “techwithtim” https://github.com/techwithtim/Flask-Web-App-Tutorial. I want to say thank you for education and content you put out on a daily.

Improved Features listed below:

Security
- CSRF protection for all forms
- Session management with 20-minute timeout
- Account lockout after 3 failed login attempts
- Password hashing using PBKDF2-SHA256
- Input sanitization and validation
- Rate limiting to prevent DoS attacks
- Secure cookie configuration
- SQL injection prevention through SQLAlchemy

User Management
- User registration with email validation
- Secure login system
- Password requirements:
  - Minimum 8 characters
  - Must contain uppercase and lowercase letters
  - Must contain numbers and special characters
- Account lockout system
- Session timeout protection

Notes
- Create, Read, Update and Delete personal notes (CRUD)
- Notes are associated with user accounts
- Real-time updates
- Confirmation before deletion

Prerequisites
- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Limiter
- Passlib
- Werkzeug
- Markupsafe
- Datetime
- Jinja2

Installation:

1. Clone the repository:

git clone https://github.com/demoh77/Web-Project.git

cd '.\Web-Project\'

2. Create a virtual environment and activate it:

python -m venv ca2
.\ca2\Scripts\activate # On Windows

3. Install the required packages:

pip install -r requirements.txt

4. Run the application:

python.exe .\main.py

The application will be available at `http://127.0.0.1:5000`

Configuration:

The application uses several configuration settings that can be modified in `__init__.py`:

```python
app.config['SECRET_KEY'] = secrets.token_hex(32) # Secret key generation for the protection of cookies
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # Prevent SQL Injection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20) # Permanent Session set to 20mins
app.config['FAILED_LOGIN_ATTEMPTS'] = 3  # Maximum failed login attempts
app.config['ACCOUNT_LOCKOUT_DURATION'] = 5  # Lockout duration in minutes
```

Project Structure:
```
Web-Project/
+-- ca2/
¦   +-- __init__.py       # Application factory, initializes the app and extensions
¦   +-- auth.py           # Handles authentication (login, signup, logout)
¦   +-- models.py         # Database models for Users and Notes
¦   +-- views.py          # Application logic for notes management
¦   +-- templates/        # HTML templates for rendering the frontend
¦       +-- base.html     # Base layout for consistent design
¦       +-- home.html     # User home page for managing notes
¦       +-- login.html    # Login page
¦       +-- sign_up.html  # Signup page
+-- main.py               # Entry point to start the application
+-- requirement.txt       # List of dependencies for the project
+-- README.md             # Project overview and Information guide
```
Security Features Explained:
Session Management
- Sessions expire after 20 minutes of inactivity
- Secure cookie configuration with HTTPOnly and SameSite flags
- Session regeneration on login

Account Protection
- Account lockout for 5 minutes after 3 failed login attempts
- Rate limiting on login and note creation endpoints
- Password complexity requirements enforced

Input Validation
- Email validation using regex
- Input sanitization for all user inputs
- XSS protection through template escaping
- CSRF tokens for all forms

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
- Flask documentation and community
- SQLAlchemy documentation
- Flask-Login documentation
- T. Ruscica, “GitHub - techwithtim/Flask-Web-App-Tutorial: Code for the note storing flask web app made during a YouTube video.,” GitHub, Jun. 15, 2021. https://github.com/techwithtim/Flask-Web-App-Tutorial 
