import sqlite3
from flask import Flask, render_template, redirect

app = Flask(__name__)

COFFEES = [
    ("Ethiopian Yirgacheffe", 125),
    ("Sumatra Mandheling", 150),
    ("Cold Brew Nitro", 120),
    ("Vanilla Latte", 125),
    ("Mexican Chiapas", 120),
    ("Cold Brew", 50),
    ("Pava Ator", 30)
]

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        votes INTEGER DEFAULT 0
    )
    ''')
    cur.execute("SELECT COUNT(*) FROM items")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO items(name,votes) VALUES(?,?)",
            COFFEES
        )
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM items ORDER BY votes DESC")
    items = cur.fetchall()
    conn.close()
    return render_template("index.html", items=items)

@app.route('/vote/<int:item_id>', methods=['POST'])
def vote(item_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE items SET votes=votes+1 WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
