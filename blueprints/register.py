from flask import Blueprint,render_template
bp = Blueprint("register",__name__,url_prefix="/register")


@bp.route("/register")
def register():
    id=123
    passwd=123
    return render_template("register.html",id=id,passwd=passwd)