from flask import Blueprint, render_template, session, request
from flask_paginate import get_page_parameter, Pagination

import config
from exts import db
bp = Blueprint("video", __name__, url_prefix="/")

@bp.route("/", defaults={'page': 1})
@bp.route("/<page>")
def index(page):
    user = session.get("name")
    print(user)
    str = "select * from video_list"

    # 分页语句
    limitpart = " LIMIT {limit} offset {offset} "

    # 每页记录行数定为9
    limit = 9

    # 获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=int(page))

    # 判断当前行和偏移量
    offset = (9 * int(page) - 9)

    # 获取总页数
    sqlcount = "select count(*) from ( "+ str+" )t1"
    total = db.session.execute(sqlcount).fetchone()[0]

    # 获取当前页的SQL语句
    sql = str + limitpart
    sql=sql.format(limit=limit, offset=offset)
    video_list = db.session.execute(sql)

    # 获取分页代码
    paginate= Pagination(page=page, total=total, per_page=9)

    return render_template("index.html", user=user, video_list=video_list, paginate=paginate)


@bp.route("/detail")
def detail():
    vid = request.args.get("vid")
    sql = "select * from video_list where video_id="+vid
    video_list = db.session.execute(sql)
    return render_template("detail.html",video_list=video_list)
