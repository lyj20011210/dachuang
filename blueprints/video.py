import json
from decimal import Decimal

from flask import Blueprint, render_template, session, request, redirect, url_for, flash
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
        if user is None:
            user = "未登录"
        # print(user)
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
        # print(video_list)
        # 获取分页代码
        video_list = list(video_list)
        # print(video_list)
        paginate = Pagination(page=page, total=total, per_page=9)
        return render_template("index.html", user=user, video_list=video_list, paginate=paginate)
    else:
        ScoreMatrix = fun.getScoreMatrix()
        video_id_list = []
        for i in ScoreMatrix:
            video_id_list.append(int(i[0]))
        videolist = []
        for i in video_id_list:
            j = str(i)
            sql = "select * from video_list where video_id=" + j
            k = db.session.execute(sql)
            k = list(k)
            k = k[0]
            videolist.append(k)
        n = 0
        for i in ScoreMatrix:
            i[1] = Decimal(str(round(i[1], 4))) * 100
            # print(i)
        # print("videolist:", videolist)
        user = session.get("name")
        total = len(videolist)
        # 每页记录行数定为9
        limit = 9
        # 获取当前页码
        page = request.args.get(get_page_parameter(), type=int, default=int(page))
        # 判断当前行和偏移量
        offset = (9 * int(page) - 9)
        video_list = videolist[offset:offset + limit:1]
        # 获取分页代码
        paginate = Pagination(page=page, total=total, per_page=9)
        return render_template("index.html", user=user, video_list=video_list, paginate=paginate, score=ScoreMatrix)


# 搜索功能
@bp.route('/search/<int:page>/')
def search(page=1):
    user = session.get("name")

    select_type = request.args["type"]
    search_content = request.args["content"]
    sql = "select * from video_list where  {}  like '%{}%'".format(select_type, search_content)
    print(sql)
    videolist = list(db.session.execute(sql))
    print("videolist", videolist)

    total = len(videolist)
    # 每页记录行数定为9
    limit = 9
    # 判断当前行和偏移量
    offset = (9 * int(page) - 9)
    videolist = videolist[offset:offset + limit:1]
    # 获取分页代码
    paginate = Pagination(page=page, total=total, per_page=9)

    return render_template("search.html", user=user, video_list=videolist, paginate=paginate)


# 转到视频播放页面
@bp.route("/detail")
def detail():
    vid = request.args.get("vid")
    session['vid'] = vid
    sql = "select * from video_list where video_id=" + vid
    video_list = db.session.execute(sql)
    sql = "select * from giveVideoScore"
    scorelist = db.session.execute(sql)
    scorelist = list(scorelist)
    name = session.get("name")
    score = "未评分"
    vid = int(vid)
    for i in scorelist:
        print(i)
        if i[1] == name:
            if i[2] == vid:
                score = i[3]
                print(score)
                break;
    return render_template("detail.html", video_list=video_list, score=score)


@bp.route("/score", methods=['GET', 'POST'])
def score():
    score = request.args.get('name')
    username = session.get("name")
    vid = session.get('vid')
    vid = int(vid)
    sql = "select * from giveVideoScore "
    flag = db.session.execute(sql)
    flag = list(flag)
    if username is None:
        flash("你还未登录")
        return "hello"
    # print(flag)
    for i in flag:
        if i[1] == username:
            if i[2] == vid:
                sql = "update giveVideoScore set score=" + score + " where user='" + username + "' and videoid=" + str(
                    vid)
                # print(sql)
                db.session.execute(sql)
                db.session.commit()
                return "hello"
    sql = "insert into giveVideoScore(user, videoid, score) values('" + username + "'," + str(vid) + "," + score + ")"
    # print(sql)
    db.session.execute(sql)
    db.session.commit()
    return redirect(url_for('detail'))
