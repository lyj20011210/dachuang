from flask import Blueprint, render_template, session, redirect, url_for, request
from exts import db
import funtion

bp = Blueprint("map", __name__, url_prefix="/map")


@bp.route("/", methods=['GET', 'POST'])
def mapindex():
    if session.get('name') is not None:
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
            current=mylabel
        # s = "select * from video_list"
        # videolist = list(db.session.execute(s))
        return render_template('Map.html', current=current, videolist=videolist, cql=cql)
    else:
        return redirect(url_for('login.login'))



@bp.route("/select",methods=['GET','POST'])
def select():
    if session.get('name') is not None:
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
            current=tap
        # s = "select * from video_list"
        # videolist = list(db.session.execute(s))
        return render_template('Map.html', current=current, videolist=videolist, cql=cql)
    else:
        return redirect(url_for('login.login'))
    # name = session.get('name')
    # s = "select * from UserMap where userid= '" + name + "'"
    # data = db.session.execute(s)
    # data = list(data)
    # print(data)
    #
    # return "select"


# 用于做标签选择和mapindex的中间跳转，这样就可以在mapindex中判断是否选择标签
@bp.route("/progress", methods=['GET', 'POST'])
def progress():
    print("progress")
    myLabel = request.form.getlist('ggg')
    myLabel = str(myLabel[0])
    print(myLabel)
    current = myLabel
    name = session.get('name')
    name = str(name)
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
    return redirect(url_for('map.mapindex'))


@bp.route("/entertap")
def enter():
    if session.get('name') is not None:
        tap = db.session.execute("select * from label")
        tap = list(tap)
        print(tap)
        taplist = []
        for i in tap:
            taplist.append(i[0])
        print(taplist)
        # return "hello"
        return render_template('MapLabel.html', taplist=taplist)
    else:
        return redirect(url_for('login.login'))
