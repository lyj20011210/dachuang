from exts import db

#用户的数据库模型
class UserModel(db.Model):
    __tablename__="user"
    id= db.Column
    