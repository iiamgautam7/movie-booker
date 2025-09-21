from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from config import DB_PATH, FLASK_BASE, FLASK_HOST, FLASK_PORT

app = Flask(__name__)
app.secret_key = "supersecret"

MOVIES = {
    "Interstellar": ["10:00 AM", "1:00 PM", "6:00 PM"],
    "Inception": ["11:00 AM", "2:00 PM", "7:00 PM"],
    "The Matrix": ["12:00 PM", "3:00 PM", "8:00 PM"]
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", movies=MOVIES)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Very simple auth for demo: just capture username
        username = request.form.get("username", "").strip()
        if username:
            session["user"] = username
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/movie/<movie_name>", methods=["GET", "POST"])
def movie_page(movie_name):
    if movie_name not in MOVIES:
        return "Movie not found", 404
    if request.method == "POST":
        if "user" not in session:
            return redirect(url_for("login"))
        showtime = request.form.get("showtime")
        username = session["user"]
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO requests (username, movie, showtime) VALUES (?, ?, ?)",
                  (username, movie_name, showtime))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("movie.html", movie=movie_name, times=MOVIES[movie_name])

@app.route("/requests")
def view_requests():
    conn = get_db()
    rows = conn.execute("SELECT * FROM requests ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("requests.html", requests=rows)

if __name__ == "_main_":
    # create DB on first run
    import db_init
    db_init.init_db()
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)