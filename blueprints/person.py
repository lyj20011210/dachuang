from flask import Blueprint,render_template

from exts import mail
from flask_mail import Message
#url_prefix:作为前缀 127.0.0.1:5000/person
bp = Blueprint("person",__name__,url_prefix="/person")

@bp.route("/person")
def person():
    return render_template("person.html")
