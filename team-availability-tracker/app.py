
import sqlite3
from flask import Flask, render_template, redirect
app = Flask(__name__)

def init_db():
    conn=sqlite3.connect("team.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,available INTEGER DEFAULT 0)")
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0]==0:
        cur.executemany("INSERT INTO users(name,available) VALUES(?,?)",
        [("Alice",1),("Bob",0),("Charlie",1),("David",0),("Emma",1)])
    conn.commit(); conn.close()

@app.route("/")
def home():
    conn=sqlite3.connect("team.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users")
    users=cur.fetchall()
    conn.close()
    return render_template("index.html",users=users)

@app.route("/toggle/<int:user_id>",methods=["POST"])
def toggle(user_id):
    conn=sqlite3.connect("team.db")
    cur=conn.cursor()
    cur.execute("UPDATE users SET available=CASE WHEN available=1 THEN 0 ELSE 1 END WHERE id=?", (user_id,))
    conn.commit(); conn.close()
    return redirect("/")

if __name__=="__main__":
    init_db()
    app.run(debug=True)
