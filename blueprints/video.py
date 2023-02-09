from decimal import Decimal

from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from flask_paginate import get_page_parameter, Pagination
import funtion as fun
from exts import db

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
        # w = fun.similarity()
        # print(w)
        ScoreMatrix = fun.getScoreMatrix()  # 此变量是已经经过余弦相似度得到的评分矩阵，甚至已经排序好了
        video_id_list = []
        for i in ScoreMatrix:
            video_id_list.append(int(i[0]))  # 把已经排序好的评分矩阵
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
    search_content = request.args["search_content"]
    sql = "select * from video_list where  video_name like '%{}%'".format(search_content)
    videolist = list(db.session.execute(sql))
    total = len(videolist)
    # 每页记录行数定为9
    limit = 9
    # 判断当前行和偏移量
    offset = (9 * int(page) - 9)
    videolist = videolist[offset:offset + limit:1]
    # 获取分页代码
    paginate = Pagination(page=page, total=total, per_page=9)
    return render_template("search.html", user=user, video_list=videolist,paginate=paginate)


# 转到视频播放页面
@bp.route("/detail")
def detail():
    user = session.get("name")
    vid = request.args.get("vid")
    session['vid'] = vid

    video_item = list(db.session.execute("select * from video_list where video_id=" + vid))
    sql = "select * from giveVideoScore"
    scorelist = db.session.execute(sql)
    scorelist = list(scorelist)
    name = session.get("name")
    score = "未评分"
    vid = int(vid)
    for i in scorelist:
        if i[1] == name:
            if i[2] == vid:
                score = i[3]
                print(score)
                break
    comment_item = list(db.session.execute("select * from comment_list where video_id=" + str(vid)))
    comment_child_item = list(db.session.execute("select * from comment_child_list"))
    length = len(comment_item)
    data = {"video_item": video_item, "comment_item": comment_item, "comment_child_item": comment_child_item,
            "length": length}
    return render_template("detail.html", user=user, score=score, data=data)


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


# 评论
@bp.route('/news_comment', methods=['POST'])
def news_comment():
    # 判断用户是否登录
    username = session.get("name")
    if username is None:
        return jsonify(errno=1, errmsg='登录后才能评论哦!')

    # 获取参数
    video_id = session.get('vid')
    content = request.json.get('content')
    parent_id = str(request.json.get('parent_id'))
    content_child = request.json.get('content_child')
    has_child = 0

    if not all([content, content_child]):
        if content == '':
            return jsonify(errno=2, errmsg='请输入评论内容!')
        if content_child == '':
            return jsonify(errno=3, errmsg='请输入回复内容!')
    # 评论回复
    if all([parent_id, content_child]):
        try:
            has_child = 1
            sql1 = "update comment_list set has_child=" + str(has_child) + " where id=" + parent_id
            sql2 = "insert into comment_child_list(username,parent_id,content) values('" + username + "', " + parent_id + " ,'" + content_child + "') "
            db.session.execute(sql1)
            db.session.execute(sql2)
            db.session.commit()
        except Exception as e:
            print("回复失败!")

    # 发表评论
    if all([video_id, content]):
        try:
            sql1 = "update video_list  set has_comment=1 where video_id=" + video_id
            sql2 = " insert into comment_list(video_id,username,content,has_child) values(" + video_id + ", '" + username + "', '" + content + "'," + str(
                has_child) + ")"
            db.session.execute(sql1)
            db.session.execute(sql2)
            db.session.commit()
        except Exception as e:
            print("评论失败!")

    return redirect(url_for('video.detail'))
