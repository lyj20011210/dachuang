# 用户的数据库模型
from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)
    signature = db.Column(db.String(300), nullable=False)  #用户个性签名
    nick_name = db.Column(db.String(200), nullable=False)  #用户昵称
    gender = db.Column(db.Enum("男", "女"), default="男")   #用户性别


# class UserInfo(db.Model):
#     __tablename__ = "user_info"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)#用户id
#     signature = db.Column(db.String(300), nullable=False)  #用户个性签名
#     nick_name = db.Column(db.String(200), nullable=False)  #用户昵称
#     gender = db.Column(db.Enum("男", "女"), default="男")   #用户性别




class Videos_List(db.Model):
    __tablename__ = "videos_list"
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_name = db.Column(db.String(200))
    video_link = db.Column(db.String(200))
    video_view = db.Column(db.String(200))
    video_comments = db.Column(db.String(200))
    video_publishedtime = db.Column(db.String(200))
