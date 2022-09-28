from flask import Blueprint,render_template
from Models import UserModel
bp = Blueprint("register",__name__,url_prefix="/register")


@bp.route("/register")
def register():

    return render_template("register.html")