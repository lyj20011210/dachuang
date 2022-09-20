from flask import Blueprint,render_template

bp=Blueprint("video",__name__,url_prefix="/")



@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/detail")
def detail():
    return render_template("detail.html")