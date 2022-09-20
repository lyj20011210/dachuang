# 数据库配置信息
HOSTNAME = 'gz-cynosdbmysql-grp-o9nzvt3p.sql.tencentcdb.com'
PORT = '23303'
DATABASE = 'Test'
USERNAME = 'root'
PASSWORD = '@L12345678'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME,
                                                 PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "HELLOWORD"
