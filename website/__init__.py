from flask import Flask, render_template, request, redirect, url_for, session
import re
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#creating database
db= SQLAlchemy()
DB_NAME="database.db"

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] ='asfsdfdfgfdfdfgrrds'
    #configuring database
    app.config["SQLALCHEMY_DATABASE_URI"]=f'sqlite:///{DB_NAME}'
    db.init_app(app)
    #registering the blueprint

    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prifix='/')
    app.register_blueprint(auth, url_prifix='/')

    #create dataabse
    from .model import User, Note
    with app.app_context():
        db.create_all()

    login_manager= LoginManager()
    #wehere shoud the route redirect if you are not login
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def login_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    
    if not path.exists('website/'+ DB_NAME):
        db.create_all(app=app)
        print('Database created')