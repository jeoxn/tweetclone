from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'tweet.db'

UPLOAD_FOLDER = 'C:/Users/axell/OneDrive/Desktop/Projects/tweetclone/website/static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .urls import urls
    from .auth import auth

    app.register_blueprint(urls)
    app.register_blueprint(auth)


    from .models import User, Tweet, Comment, Like, Follow

    with app.app_context():
        db.init_app(app)
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def login_manager(id):
        return User.query.get(int(id))

    return app


