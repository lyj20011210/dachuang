from flask import Blueprint, render_template, session

bp=Blueprint("video",__name__,url_prefix="/")



@bp.route("/")
def index():
    user=session.get("name")
    print(user)
    return render_template("index.html",user=user)

@bp.route("/detail")
def detail():
    return render_template("detail.html")