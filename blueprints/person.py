from flask import Blueprint, render_template, redirect, request, jsonify, current_app, session, url_for, g
from sqlalchemy.testing import db

from exts import mail
from flask_mail import Message

# url_prefix:作为前缀 127.0.0.1:5000/person
bp = Blueprint("person", __name__, url_prefix="/person")


@bp.route("/person")
def person():
    return render_template("person.html")


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
