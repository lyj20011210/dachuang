from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_paginate import get_page_parameter, Pagination
import funtion as fun
import config
from exts import db
import numpy as np

bp = Blueprint("video", __name__, url_prefix="/")


@bp.route("/", defaults={'page': 1})
@bp.route("/<page>")
def index(page):
    if session.get("name") is None:
        user = session.get("name")
        print(user)
        sql = "select * from video_list"
        # 分页语句
        limitpart = " LIMIT {limit} offset {offset} "
        # 每页记录行数定为9
        limit = 9
        # 获取当前页码
        page = request.args.get(get_page_parameter(), type=int, default=int(page))
        # 判断当前行和偏移量
        offset = (9 * int(page) - 9)
        # 获取总页数
        sqlcount = "select count(*) from ( " + sql + " )t1"
        total = db.session.execute(sqlcount).fetchone()[0]
        # 获取当前页的SQL语句
        sql = sql + limitpart
        sql = sql.format(limit=limit, offset=offset)
        video_list = db.session.execute(sql)
        print(video_list)
        # 获取分页代码
        video_list=list(video_list)
        print(video_list)
        paginate = Pagination(page=page, total=total, per_page=9)
        return render_template("index.html", user=user, video_list=video_list, paginate=paginate)
    else:
        sql = "select * from user_interest where user_name= '" + session.get("name") + "'"
        print(sql)
        usertag = db.session.execute(sql)
        usertag = list(usertag)
        print(usertag)
        sql = "select * from videos_interest"
        videotag = db.session.execute(sql)
        videotag = list(videotag)
        print(videotag)
        num = db.session.execute("select count(*) from videos_interest")
        num = list(num)
        num = num[0][0]
        ScoreMatrix = fun.count(usertag, videotag, num)
        n = 0
        while True:
            if n == num:
                break
            m = 0
            while True:
                if m + 1 == num:
                    break
                if ScoreMatrix[m][1] < ScoreMatrix[m + 1][1]:
                    temp = np.zeros(2)
                    temp[0] = ScoreMatrix[m][0]
                    temp[1] = ScoreMatrix[m][1]
                    ScoreMatrix[m] = ScoreMatrix[m + 1]
                    ScoreMatrix[m + 1] = [temp[0], temp[1]]
                m = m + 1
            n = n + 1
        video_id_list = []
        for i in ScoreMatrix:
            video_id_list.append(int(i[0]))
        videolist=[]
        for i in video_id_list:
            j = str(i)
            sql = "select * from video_list where video_id=" + j
            k=db.session.execute(sql)
            k=list(k)
            k=k[0]
            videolist.append(k)
        print(videolist)
        user = session.get("name")
        sql = "select * from video_list"
        # 分页语句
        limitpart = " LIMIT {limit} offset {offset} "
        # 每页记录行数定为9
        limit = 9
        # 获取当前页码
        page = request.args.get(get_page_parameter(), type=int, default=int(page))
        # 判断当前行和偏移量
        offset = (9 * int(page) - 9)
        # 获取总页数
        sqlcount = "select count(*) from ( " + sql + " )t1"
        total = db.session.execute(sqlcount).fetchone()[0]
        # 获取当前页的SQL语句
        sql = sql + limitpart
        sql = sql.format(limit=limit, offset=offset)
        # 获取分页代码
        paginate = Pagination(page=page, total=total, per_page=9)
        return render_template("index.html", user=user, video_list=videolist, paginate=paginate)


@bp.route("/detail")
def detail():
    vid = request.args.get("vid")
    sql = "select * from video_list where video_id=" + vid
    video_list = db.session.execute(sql)
    return render_template("detail.html", video_list=video_list)
