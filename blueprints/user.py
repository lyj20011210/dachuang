from flask import Blueprint,render_template

#url_prefix:作为前缀 127.0.0.1:5000/user
bp = Blueprint("user",__name__,url_prefix="/user")

@bp.route("/login")
def login():
    return render_template("Login.html")

@bp.route("/register")
def register():
    return render_template("register.html")