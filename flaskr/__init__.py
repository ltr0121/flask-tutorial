import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) ## Flask 인스턴스 생성 name은 현재 python module
    app.config.from_mapping( ## 환경 설정
        SECRET_KEY='dev', ## 데이터 보안 유지
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite') ##SQLite 데이터베이스 파일 저장할 경로
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello') ## create connection
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app