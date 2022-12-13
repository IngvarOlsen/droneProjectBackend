from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

# # Create a SQLAlchemy engine that points to the SQLite database
# engine = create_engine('sqlite:///database.db')

# # Create a MetaData object
# metadata = MetaData()


# # Bind the MetaData object to the SQLite database using the engine
# metadata.bind = engine
# # Reflect the schema of the database into the MetaData object
# metadata.reflect() 
# # Create a base class for your SQLAlchemy models
# Base = declarative_base(metadata=metadata)

# # Create a session to manage your database
# Session = sessionmaker(bind=engine)
# session = Session()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api
    

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/')

   # from .models import User, Note
    from .models import User, Job, Image, ImageSet, RenderedModel

    with app.app_context():
        db.create_all()
    # create_database(app)

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
        print('Created Database!')
