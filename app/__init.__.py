from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()
DB_NAME = "spotifyJournal.db"

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config["SESSION_COOKIE_NAME"] = 'My Journal'

    from .routes.views import views
    from .routes.auth import auth
    from .routes.spotify import spotify

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(spotify, url_prefix='/spotify')


    return app