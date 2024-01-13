from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    from app.views.Login import login_view as login_view_blueprint
    app.register_blueprint(login_view_blueprint)
    return app
