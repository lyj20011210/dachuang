from flask import Flask
import config
from exts import db,mail
# 在此导入蓝图
from blueprints import login_bp, video_bp,register_bp, person_bp

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
# 在此注册蓝图
app.register_blueprint(login_bp)
app.register_blueprint(video_bp)
app.register_blueprint(register_bp)
app.register_blueprint(person_bp)

if __name__ == '__main__':
    app.run(debug=True)
