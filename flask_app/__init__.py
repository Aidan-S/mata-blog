# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_talisman import Talisman
from flask_mongoengine import MongoEngine
from flask_mail import Mail, Message
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os



db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail(Flask(__name__))


from .users.routes import users
from .posts.routes import posts


def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    csp = {
        'default-src': [
            '\'self\'',
            'https://stackpath.com',
            'https://code.jquery.com',
            'https://cdn.jsdelivr.net',
            'https://stackpath.bootstrapcdn.com'
        ]
    }

    Talisman(app, content_security_policy=csp)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_SENDER'] = os.environ.get('MAIL_SENDER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')


    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app
