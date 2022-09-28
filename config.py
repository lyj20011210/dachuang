# 数据库配置信息
from urllib import parse

HOSTNAME = 'gz-cynosdbmysql-grp-o9nzvt3p.sql.tencentcdb.com'
PORT = '23303'
DATABASE = 'Test'
USERNAME = 'root'
PASSWORD = '@L12345678'
pwd = parse.quote_plus(PASSWORD)
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, pwd, HOSTNAME,
                                                 PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "HELLOWORD"
