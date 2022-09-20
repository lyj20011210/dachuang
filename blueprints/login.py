from flask import Blueprint,render_template

from exts import mail
from flask_mail import Message
#url_prefix:作为前缀 127.0.0.1:5000/user
bp = Blueprint("login",__name__,url_prefix="/user")

@bp.route("/login")
def login():
    return render_template("Login.html")

@bp.route("/mail")
def my_mail():
    message = Message(
        subject="邮箱测试",
        recipients=['1252967009@qq.com'],
        body="这是一篇测试邮件"
    )
    mail.send(message)
    return "success"
@bp.route("/person")
def person():
    return render_template("person.html")
