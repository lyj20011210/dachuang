from flask import Blueprint,render_template

bp=Blueprint("user",__name__,url_prefix="/user")



@bp.route("/login")
def login():
    return render_template("Login.html")

@bp.route("/register")
def register():
    return render_template("register.html")