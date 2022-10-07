from flask import Blueprint, render_template, request, redirect, url_for, flash
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
        sql="select count(*) from user where username='"+request.form.get('id')+"'"
        flag=int(list(db.session.execute(sql))[0][0])
        print(flag)
        if flag!=0:
            flash("用户名已存在")
            return redirect(url_for('register.register'))
        if passwd2!=passwd1:
            flash('两次输入的密码不一致')
            return redirect(url_for('register.register'))
        sql="insert into user_interest(user_name) values('"+request.form.get('id')+"')"
        db.session.add(user)
        db.session.execute(sql)
        db.session.commit()
        return redirect(url_for("login.login"))


