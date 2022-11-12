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
        str = "select * from label"
        sql = db.session.execute(str)
        sql = list(sql)
        taplist = []
        for i in sql:
            # taplist内含全部标签信息
            taplist.append(i[0])
        str = "select * from user_interest where user_name= '" + session.get("name") + "'"
        persontap = db.session.execute(str)
        persontap = list(persontap)
        # print(persontap)
        showtap = []
        for i in taplist:
            # 对该用户元祖的每个标签列逐一遍历，若发现标签列值为1，则取出该标签名
            str = "select " + i + " from user_interest where user_name = '" + session.get("name") + "'"
            # print(str)
            j = db.session.execute(str)
            j = list(j)
            j = int(j[0][0])
            if j == 1:
                showtap.append(i)
        # print(showtap)
        return render_template("person.html", taplist=taplist, name=session.get("name"), showtap=showtap)
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
        str = "update user_interest set " + i + " = 0 where user_name ='" + session.get("name") + "'"
        db.session.execute(str);
    for i in myLabel:
        str = "update user_interest set " + i + " = 1 where user_name = '" + session.get("name") + "'"
        db.session.execute(str)
    db.session.commit()
    return redirect(url_for('person.person'))


@bp.route("/collects")
def collects():
    # print("测试点1")
    if session.get("name") is not None:
        user = session.get("name")
        str = "select * from user_collects where user= '" + user + "'"
        sql = db.session.execute(str)
        sql = list(sql)
        vid = []
        collect = []
        for i in sql:
            if i[3] == 1:
                vid.append(i[2])
        print(vid)
        for i in vid:
            str = "select * from video_list where video_id= ' +i+ '"
            sql = db.session.execute(str)
            if sql == "":
                print("sql错误")
            collect.append(sql)
        return render_template("person.html", user=user, collect_list=collect, name=session.get("name"))
    else:
        return redirect(url_for('login.login'))
