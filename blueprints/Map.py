from flask import Blueprint, render_template, session, redirect, url_for, request
from exts import db

bp = Blueprint("map", __name__, url_prefix="/map")


@bp.route("/",methods=['GET','POST'])
def mapindex():
    if session.get('name') != None:
        myLabel = request.form.getlist('tap')
        myLabel=str(myLabel[0])
        print(myLabel)
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
            s = "insert into UserMap(userid,tap) values ('" + name +"','"+myLabel+"')"
            print(s)
            db.session.execute(s)
            db.session.commit()
        else:
            s = "update UserMap SET tap='" +myLabel+"'where userid='"+name+"'"
            db.session.execute(s)
            db.session.commit()
            print(s)
        return render_template('Map.html',data=myLabel)
    else:
        return redirect(url_for('login.login'))


@bp.route("/entertap")
def enter():
    tap = db.session.execute("select * from label")
    tap = list(tap)
    print(tap)
    taplist = []
    for i in tap:
        taplist.append(i[0])
    print(taplist)
    # return "hello"
    return render_template('MapLabel.html', taplist=taplist)
