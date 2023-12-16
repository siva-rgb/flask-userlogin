from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import User
from werkzeug.security import generate_password_hash, check_password_hash
from .import db
from flask_login import login_user, login_required, logout_user, current_user


auth= Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data= request.form
    user_name= data.get('username')
    password= data.get('password')

    user= User.query.filter_by(user_name=user_name).first()
    if user:
        if check_password_hash(user.password, password):
            flash('Login Successful', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect Username or password', category='error')
    else:
        flash('Username does not Exist', category='error')
    return render_template("login.html",cur_user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    #geting user information in form
    if request.method == 'POST':

        data= request.form
        user_name= data.get('username')
        email= data.get('email')
        password= data.get('password')
        confirm= data.get('confirm')
        user= User.query.filter_by(user_name=user_name).first()
        if user:
            flash('User Already Exist', category='error')
        if len(email)<4:
            flash('Email must be greater than 4 character', category= 'error')
        elif len(user_name)<2:
            flash('Username must be greater than 2 character', category= 'error')
        elif password != confirm:
            flash('Password not matching ', category= 'error')
        else:
            #create user 
            new_user= User(email=email, password=generate_password_hash(password, method='pbkdf2', salt_length=16), user_name=user_name) 
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('User Created Successfully', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", cur_user= current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))