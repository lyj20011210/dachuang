from flask import Blueprint, render_template, redirect, request, jsonify, current_app, session, url_for, g

from Models import Videos_List
from exts import db

from exts import mail
from flask_mail import Message

# url_prefix:作为前缀 127.0.0.1:5000/person
bp = Blueprint("person", __name__, url_prefix="/person")


@bp.route("/person")
def person():
    # 读取全部的标签并且输出到页面上
    if session.get("name") != None:
        s = "select * from label"
        sql = db.session.execute(s)
        sql = list(sql)
        taplist = []
        for i in sql:
            # taplist内含全部标签信息
            taplist.append(i[0])
        s = "select * from user_interest where user_name= '" + session.get("name") + "'"
        persontap = db.session.execute(s)
        persontap = list(persontap)
        print(persontap)
        showtap = []
        for i in taplist:
            # 对该用户元祖的每个标签列逐一遍历，若发现标签列值为1，则取出该标签名
            s = "select " + i + " from user_interest where user_name = '" + session.get("name") + "'"
            # print(s)
            j = db.session.execute(s)
            j = list(j)
            j = int(j[0][0])
            if j == 1:
                showtap.append(i)
        # print(showtap)
        # 收藏
        user = session.get("name")
        s = "select * from user_collects where user= '" + user + "'"
        sql = db.session.execute(s)
        sql = list(sql)
        vid = []
        collects = []
        for i in sql:
            if i[3] == 1:
                vid.append(i[2])
        print(vid)
        for i in vid:
            i = str(i)
            s = "select * from video_list where video_id= " + i
            sql = db.session.execute(s)
            sql = list(sql)
            sql = sql[0]
            collects.append(sql)
        print(collects)
        return render_template("person.html", taplist=taplist, name=session.get("name"), showtap=showtap,
                               collects=collects)
    else:
        return redirect(url_for('login.login'))


@bp.route("/entertap", methods=["GET", "POST"])
def enter():
    myLabel = request.form.getlist('tap')
    # 读取到用户前端选择的标签
    allLabel = db.session.execute("select * from label")
    allLabel = list(allLabel)
    allLabel1 = []
    for i in allLabel:
        allLabel1.append(i[0])
        # 把用户所有的标签数据归零
    for i in allLabel1:
        s = "update user_interest set " + i + " = 0 where user_name ='" + session.get("name") + "'"
        db.session.execute(s);
    for i in myLabel:
        s = "update user_interest set " + i + " = 1 where user_name = '" + session.get("name") + "'"
        db.session.execute(s)
    db.session.commit()
    return redirect(url_for('person.person'))

