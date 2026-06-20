
import sqlite3
import requests
import random
from flask import Flask, render_template

app = Flask(__name__)
DB = "quotes.db"

FALLBACK_QUOTES = [
    ("Success is not final, failure is not fatal.", "Winston Churchill"),
    ("Stay hungry, stay foolish.", "Steve Jobs"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The best way to predict the future is to create it.", "Peter Drucker"),
    ("Dream big and dare to fail.", "Norman Vaughan"),
    ("Do one thing every day that scares you.", "Eleanor Roosevelt"),
    ("Action is the foundational key to all success.", "Pablo Picasso")
]

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quote_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT,
            author TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        data = response.json()[0]
        return data["q"], data["a"]
    except Exception:
        return random.choice(FALLBACK_QUOTES)

@app.route("/")
def home():
    quote, author = get_quote()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO quote_history (quote, author) VALUES (?, ?)",
        (quote, author)
    )

    conn.commit()

    cur.execute(
        "SELECT quote, author FROM quote_history ORDER BY id DESC LIMIT 10"
    )
    history = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        quote=quote,
        author=author,
        history=history
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
