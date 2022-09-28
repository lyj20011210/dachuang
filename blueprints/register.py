from flask import Blueprint, render_template, request, redirect, url_for
from Models import UserModel
from .forms import RegisterForm
from exts import db

bp = Blueprint("register", __name__, url_prefix="/register")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method=='POST':
        form = RegisterForm(request.form)
        print(request.form['id'])
        user = form.id.data
        passwd1 = form.password1.data
        passwd2 = form.password2.data
        print(passwd2)
        user = UserModel(username=user, password=passwd1)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login.login"))


