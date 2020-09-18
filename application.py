import os

from cs50 import SQL

from flask import Flask, flash, jsonify, redirect, render_template, request, session, abort
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import lookup, login_required

# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///books.db")

@app.route("/", methods=["GET", "POST"])
def index():
    import error_handler
    if request.method == "GET":
        return render_template("index.html")
    else:
        search = request.form.get('search')
        result = lookup(search)      
        if result == None:
            abort(404)
        else:
            return render_template("index.html", results=result)


@app.route("/explore", methods=["GET", "POST"])
@login_required
def explore():
    import error_handler
    if request.method == "GET":
        return render_template("explore.html")
    else:
        pass


@app.route("/bookshelf", methods=["GET", "POST"])
@login_required
def bookshelf():
    if request.method == "GET":
        return render_template("bookshelf.html")
    else:
        pass



@app.route("/login", methods=["GET", "POST"])
def login():
    import error_handler
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            abort(403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            abort(403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            abort(403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/") 

@app.route("/register", methods=["GET", "POST"])
def register():
    import error_handler
    """Registers users"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        if not request.form.get("name"):
           abort(403)
        #ensure user provides username
        if not request.form.get("username"):
            abort(403)
        
        #ensure user provides password
        elif not request.form.get("password"):
            abort(403)

        username = request.form.get("username")
        password = request.form.get("password")
        re_password = request.form.get("re_password")
        if password != re_password:
            abort(400)
        else:
            prim_key = db.execute("INSERT INTO users (username, password) VALUES (:name, :hash)"
            ,name=username, hash=generate_password_hash(password))
            
            if prim_key is None:
                abort(403)
            session["user_id"] = prim_key
        return redirect ("/")


