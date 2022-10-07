from flask import Blueprint, render_template, redirect, request, jsonify, current_app, session, url_for, g
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
        print(persontap)
        showtap=[]
        for i in taplist:
            #对该用户元祖的每个标签列逐一遍历，若发现标签列值为1，则取出该标签名
            str = "select "+i+" from user_interest where user_name = '" + session.get("name") + "'"
            print(str)
            j=db.session.execute(str)
            j=list(j)
            j=int(j[0][0])
            if j==1:
                showtap.append(i)
        print(showtap)
        return render_template("person.html", taplist=taplist, name=session.get("name"),showtap=showtap)
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


@bp.route("/base_info", methods=["GET", "POST"])
def base_info():
    """
    用户信息基本设置
    用户是否登录
    GET请求:
        查询到性别返回到前端进行展示
    POST请求:
        接收参数,注意给默认值
        昵称和性别必须要传齐
        校验性别是否合法
        保存到数据库
    将session的值进行修改
    返回结果
    :return:
    """
    # 用户是否登录
    user = g.user
    if not user:
        redirect(url_for("index.index"))

    # GET请求:
    if request.method == "GET":
        context = {
            "user": user.to_dict()
        }
        return render_template("news/user_base_info.html", context=context)
    # POST请求:
    #     接收参数,注意给默认值
    if request.method == "POST":
        signature = request.json.get("signature", "")
        nick_name = request.json.get("nick_name")
        gender = request.json.get("gender")

        #     昵称和性别必须要传齐
        if not all([nick_name, gender]):
            return jsonify(errno="RET.PARAMERR", errmsg="参数缺少")

        # 校验性别是否合法
        if not gender in ["WOMAN", "MAN"]:
            return jsonify(errno="RET.PARAMERR", errmsg="参数异常")
        #     保存到数据库
        user.signature = signature
        user.nick_name = nick_name
        user.gender = gender
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return jsonify(errno="RET.DBERR", errmsg="修改失败")
        # 将session的值进行修改
        session["nick_name"] = nick_name
        return jsonify(errno="RET.OK", errmsg="成功")
