import json
import re
from decimal import Decimal

import datetime
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from flask_paginate import get_page_parameter, Pagination
import funtion as fun
from exts import db

bp = Blueprint("video", __name__, url_prefix="/")


@bp.route("/", defaults={'page': 1})
@bp.route("/<page>")
def index(page):
    # time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print("start " + time)
    if session.get("name") is None:
        user = session.get("name")
        if user is None:
            user = "未登录"

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

        # 获取分页代码
        video_list = list(video_list)
        paginate = Pagination(page=page, total=total, per_page=9)
        return render_template("index.html", user=user, video_list=video_list, paginate=paginate)
    else:
        ScoreMatrix = fun.getScoreMatrix()  # 此变量是已经经过余弦相似度得到的评分矩阵，甚至已经排序好了
        video_id_list = []
        for i in ScoreMatrix:
            video_id_list.append(int(i[0]))  # 把已经排序好的评分矩阵

        sql = "select video_id,video_image,video_name,video_author,video_publishedtime from video_list"
        list1 = db.session.execute(sql)
        list1 = list(list1)
        index_dict = {value: index for index, value in enumerate(video_id_list)}
        videolist = sorted(list1, key=lambda x: index_dict[x[0]])
        for i in ScoreMatrix:
            # print(i[1])
            i[1] = Decimal(str(round(i[1], 4))) * 100

        user = session.get("name")
        total = len(videolist)
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
@bp.route('/search')
def search():
    if session.get("name") is None:
        user = session.get("name")
        if user is None:
            user = "未登录"
        search_content = request.args["search_content"]
        sql = "select * from video_list where  video_name like '%{}%'".format(search_content)
        videolist = list(db.session.execute(sql))
        return render_template("search.html", user=user, video_list=videolist)
    else:
        ScoreMatrix = fun.getScoreMatrix()  # 此变量是已经经过余弦相似度得到的评分矩阵，甚至已经排序好了
        video_id_list = []
        for i in ScoreMatrix:
            video_id_list.append(int(i[0]))  # 把已经排序好的评分矩阵

        sql = "select video_id,video_image,video_name,video_author,video_publishedtime from video_list"
        list1 = db.session.execute(sql)
        list1 = list(list1)
        index_dict = {value: index for index, value in enumerate(video_id_list)}
        videolist = sorted(list1, key=lambda x: index_dict[x[0]])
        for i in ScoreMatrix:
            # print(i[1])
            i[1] = Decimal(str(round(i[1], 4))) * 100

        user = session.get("name")
        search_content = request.args["search_content"]
        sql = "select * from video_list where  video_name like '%{}%'".format(search_content)
        videolist = list(db.session.execute(sql))
        return render_template("search.html", user=user, video_list=videolist, score=ScoreMatrix)


# 转到视频播放页面
@bp.route("/detail/<string:vid>")
def detail(vid):
    session['vid'] = vid
    video_item = list(db.session.execute("select * from video_list where video_id=" + vid))
    sql = "select * from giveVideoScore"
    scorelist = db.session.execute(sql)
    scorelist = list(scorelist)
    name = session.get("name")
    score = "未评分"
    vid = int(vid)
    for i in scorelist:
        if i['user'] == name:
            if i['videoid'] == vid:
                score = i['score']
                print(score)
                break
    comment_item = list(db.session.execute("select * from comment_list where video_id=" + str(vid)))
    comment_child_item = list(db.session.execute("select * from comment_child_list"))
    length = len(comment_item)

    # 获取同类型视频
    videotag_str = str((db.session.execute("select video_tag from video_list where video_id=" + str(vid))).all())
    start_index = videotag_str.index("(")
    end_index = videotag_str.index(")")
    videotag = videotag_str[start_index + 1:end_index - 1]
    videotag = re.sub(r"'", "", videotag)
    videotag_list = videotag.split("/")

    for x in videotag_list:
        same_video_item = list(
            db.session.execute("select * from video_list where  video_tag like " + '{}'.format("'%" + x + "%'")))
        same_video_item.extend(same_video_item)
        same_video_item = list(set(same_video_item))

    # 获取评分矩阵
    user = session.get("name")
    if user is None:
        user = "未登录"
        data = {"video_item": video_item, "comment_item": comment_item, "comment_child_item": comment_child_item,
                "length": length, "same_video_item": same_video_item}
        return render_template("detail.html", user=user, score=score, data=data)
    else:
        ScoreMatrix = fun.getScoreMatrix()  # 此变量是已经经过余弦相似度得到的评分矩阵，甚至已经排序好了
        video_id_list = []
        for i in ScoreMatrix:
            video_id_list.append(int(i[0]))  # 把已经排序好的评分矩阵

        sql = "select video_id,video_image,video_name,video_author,video_publishedtime from video_list"
        list1 = db.session.execute(sql)
        list1 = list(list1)
        index_dict = {value: index for index, value in enumerate(video_id_list)}
        videolist = sorted(list1, key=lambda x: index_dict[x[0]])
        for i in ScoreMatrix:
            # print(i[1])
            i[1] = Decimal(str(round(i[1], 4))) * 100

        data = {"video_item": video_item, "comment_item": comment_item, "comment_child_item": comment_child_item,
                "length": length, "same_video_item": same_video_item, "score": ScoreMatrix}
        return render_template("detail.html", user=user, score=score, data=data)


@bp.route("/score", methods=['GET', 'POST'])
def score():
    score = request.args.get('name')
    username = session.get("name")
    sql="select id from user where username='"+str(username)+"'"
    userid=db.session.execute(sql)
    userid=list(userid)
    userid=userid[0][0]
    print(userid)
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
        if i['user'] == username:
            if i['videoid'] == vid:
                sql = "update giveVideoScore set score=" + score + " where user='" + username + "' and videoid=" + str(
                    vid)
                print(sql)
                db.session.execute(sql)
                db.session.commit()
                return redirect(url_for('detail'))
    sql = "insert into giveVideoScore(user, userid,videoid, score) values('" + username + "',"+userid+"," + str(vid) + "," + score + ")"
    print(sql)
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
    content = str(request.json.get('content'))
    parent_id = str(request.json.get('parent_id'))
    content_child = str(request.json.get('content_child'))
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
    if content == 'None':
        content = ''
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

    return redirect(url_for('video.detail', vid=video_id))


@bp.route("/collects", methods=['GET', 'POST'])
def collects():
    collect = request.args.get('flag_c')
    username = session.get("name")
    vid = session.get('vid')
    vid = int(vid)
    sql = "select * from user_collects "
    flag = db.session.execute(sql)
    flag = list(flag)
    if username is None:
        return jsonify(errno=1, errmsg='登录后才能收藏哦!')
    for i in flag:
        if i[1] == username:
            if i[2] == vid:
                if i[3] == collect:
                    return jsonify(errno=2, errmsg='已经在收藏夹!')
                sql = "update user_collects set isCollected=" + collect + " where user='" + username + "' and videoid=" + str(
                    vid)
                db.session.execute(sql)
                db.session.commit()
                return jsonify(errno=0, errmsg='成功')
    sql = "insert into user_collects(user, videoid, isCollected) values('" + username + "'," + str(
        vid) + "," + collect + ")"
    db.session.execute(sql)
    db.session.commit()
    return redirect(url_for('video.detail'), flag=flag)
