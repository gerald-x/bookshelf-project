from application import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html")

@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html")