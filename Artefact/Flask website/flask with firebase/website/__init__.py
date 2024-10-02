from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


# create app
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'sadlkjasflkjask'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # import the blueprints in views and auth
    from .views import views
    from .auth import auth

    # register these blueprints with the prefix /, which basically means they do not need a prefix
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import the User which is defined in models.py
    from .models import User

    # Create the database using function

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database created successfully')
