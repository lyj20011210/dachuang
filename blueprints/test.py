import datetime
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from flask_paginate import get_page_parameter, Pagination

import funtion
from exts import db

bp = Blueprint("test", __name__, url_prefix="/test")


@bp.route('/test')
def i():
    if session.get('name') is not None:
        tap = db.session.execute("select * from label")
        tap = list(tap)
        print(tap)
        taplist = []
        for i in tap:
            taplist.append(i[0])
        print(taplist)
        videolist = []
        name = session.get('name')
        s = "select count(*) from UserMap where userid='" + name + "'"
        count = db.session.execute(s)
        count = list(count)
        count = count[0][0]
        print("count:")
        print(count)
        # 如果还缺乏选择记录，则强制选择
        if count == 0:
            cql = "MATCH p=()-[:base]->() RETURN p LIMIT 25;"
            current = "暂无"
            print(cql)
        else:
            s = "select * from UserMap where userid='" + name + "'"
            mylabel = db.session.execute(s)
            mylabel = list(mylabel)
            mylabel = mylabel[0]
            print(mylabel)
            mylabel = mylabel[1]
            cql = "MATCH (c:Lable{name:'" + mylabel + "'})<-[r*0..]-(result) return result,r"
            print(cql)
            videolist = funtion.selectVideoWithLabel(mylabel)
            print(videolist)
            current = mylabel

        # s = "select * from video_list"
        # videolist = list(db.session.execute(s))
        return render_template('bee.html', current=current, videolist=videolist, cql=cql, taplist=taplist)
    else:
        return redirect(url_for('login.login'))


@bp.route("/select", methods=['GET', 'POST'])
def select():
    print("select")
    if session.get('name') is not None:
        name = session.get('name')
        name = str(name)
        print("progress")
        myLabel = request.form.getlist('ggg')
        if len(myLabel) == 0:
            s = "delete from UserMap where userid='" + name + "'"
            print(s)
            db.session.execute(s)
            db.session.commit()
            return redirect(url_for("test.i"))
        myLabel = str(myLabel[0])
        print(myLabel)
        user = db.session.execute("select * from UserMap")
        user = list(user)
        flag = 0
        print(name)
        for i in user:
            print(i)
            if i[0] == name:
                flag = 1
        if flag == 0:
            s = "insert into UserMap(userid,tap) values ('" + name + "','" + myLabel + "')"
            print(s)
            db.session.execute(s)
            db.session.commit()
        else:
            s = "update UserMap SET tap='" + myLabel + "'where userid='" + name + "'"
            db.session.execute(s)
            db.session.commit()
            print(s)
            return redirect(url_for("test.i"))
    else:
        return redirect(url_for('login.login'))


@bp.route("/tap", methods=['GET', 'POST'])
def tap():
    if session.get('name') is not None:
        tap = db.session.execute("select * from label")
        tap = list(tap)
        print(tap)
        taplist = []
        for i in tap:
            taplist.append(i[0])
        print(taplist)
        videolist = []
        tap = request.args.get('tap')
        name = session.get('name')
        s = "select count(*) from UserMap where userid='" + name + "'"
        count = db.session.execute(s)
        count = list(count)
        count = count[0][0]
        print("count:")
        print(count)
        # 如果还缺乏选择记录，则强制选择
        if count == 0:
            cql = "MATCH p=()-[:base]->() RETURN p LIMIT 25;"
            current = "暂无"
            print(cql)
        else:
            s = "select * from UserMap where userid='" + name + "'"
            mylabel = db.session.execute(s)
            mylabel = list(mylabel)
            mylabel = mylabel[0]
            print(mylabel)
            mylabel = mylabel[1]
            cql = "MATCH (c:Lable{name:'" + mylabel + "'})<-[r*0..]-(result) return result,r"
            print(cql)
            videolist = funtion.selectVideoWithLabel(tap)
            print(videolist)
            current = tap
        # s = "select * from video_list"
        # videolist = list(db.session.execute(s))
        return render_template('bee.html',taplist=taplist ,current=current, videolist=videolist, cql=cql)
    else:
        return redirect(url_for('login.login'))
