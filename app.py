from flask import Flask
import config
from exts import db
# 在此导入蓝图
from blueprints import user_bp, video_bp

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
# 在此注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(video_bp)

if __name__ == '__main__':
    app.run(debug=True)
