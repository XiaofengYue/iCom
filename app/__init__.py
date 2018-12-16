from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from app.config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
db = SQLAlchemy()
auth = HTTPBasicAuth()


def create_app(config_class=Config):
    app.config.from_object(Config)
    db.init_app(app)

    from app.test.routes import tests
    app.register_blueprint(tests)
    from app.user.routes import users
    app.register_blueprint(users)
    from app.role.routes import roles
    app.register_blueprint(roles)
    from app.competition.routes import competitions
    app.register_blueprint(competitions)
    from app.collection.routes import collections
    app.register_blueprint(collections)
    from app.focus.routes import focus
    app.register_blueprint(focus)
    from app.interest.routes import interests
    app.register_blueprint(interests)
    from app.RESTAURANT.routes import rests
    app.register_blueprint(rests)
    return app
