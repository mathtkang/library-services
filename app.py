import pymysql
from flask import Flask, render_template
from db_connect import db
from flask_bcrypt import Bcrypt
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    bcrypt = Bcrypt(app)

    # 블루프린트
    from views import main_view, sub_view
    app.register_blueprint(main_view.bp)
    app.register_blueprint(sub_view.bp)

    # 세션 사용시
    app.secret_key = "asdfasdfasdf"
    app.config['SESSION_TYPE'] = 'filesystem'

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=1234)
