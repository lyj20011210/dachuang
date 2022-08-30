# 数据库配置信息
HOSTNAME = '127.0.0.1'
PORT = '3307'
DATABASE = 'recommendation'
USERNAME = 'root'
PASSWORD = '12345678'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME,
                                                 PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "HELLOWORD"
