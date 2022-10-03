from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from exts import db
from .forms import LoginForm
from Models import UserModel

# url_prefix:作为前缀 127.0.0.1:5000/user
bp = Blueprint("login", __name__, url_prefix="/user")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        user = form.user.data
        password = request.form.get("password")
        finduser = UserModel.query.filter_by(username=user).first()
        if finduser:
            checkuser = finduser.username
            checkpwd = finduser.password
            password=str(password)
            if checkpwd == password:
                session["name"] = checkuser
                print(session["name"])
                return redirect("/")
            else:
                flash("密码错误")
                return redirect(url_for("login.login"))
        else:
            flash("用户不存在")
            return redirect(url_for("login.login"))
        # if checkuser == user:
        #     findpassword= UserModel.query.filter_by(password=password).first()
        #     passwordcheck=findpassword.password
        #     print(passwordcheck)
        #     if passwordcheck== password:
        #         session["name"] = checkuser
        #         return redirect("/")
        # else:
        #     flash("用户名不存在")
        #     return redirect(url_for("login.login"))
