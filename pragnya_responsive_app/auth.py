from flask import Blueprint, render_template, redirect, url_for, request, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required,current_user
auth = Blueprint('auth', __name__)

@auth.route('/login_post',methods=['GET','POST'])
def login_post():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = request.form.get('remember')
        remember = True if remember else False
        from . models import User
        user = User.query.filter_by(email=email).first()
        if user:
             username = user.name
        else:
    # Handle the case where the user is not found
            username = None  # or some default value or raise an exception
        if user and check_password_hash(user.password,password=password):
            login_user(user=user,remember=remember) 
            flash("Login Successfull!", 'success')
            return redirect(url_for("main.mainpage",username=username))
        else:
            flash("Invalid Email or password  ",'failure')
    return render_template("login_style.htm")
        

@auth.route('/signup_post', methods=['GET', 'POST'])
def signup_post():
    if request.method == 'POST':
        fname = request.form['firstName']
        lname = request.form['lastName']
        name = fname + ' ' + lname
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirmPassword"]
        hashed_password = generate_password_hash(password=password,method='pbkdf2:sha256')


        if password != confirm_password:
            flash("Passwords don't match", "error")
            return redirect(url_for("auth.signup"))
        from .models import User
        from . import db 
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash(f"User with {email} already exits!")
            return render_template("signUp.htm")
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup Successful!", 'success')
        return redirect(url_for("auth.login"))
    
    # Handle GET request: render the signup page
    return render_template('signUp.htm')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home',show_auth_buttons=True))

 

@auth.route('/login')
def login():
    return render_template('login_style.htm',show_auth_buttons=True)


@auth.route('/signup')
def signup():
    return render_template('signUp.htm',show_auth_buttons=True)

@auth.route('/Account')
@login_required
def Account():
    return render_template('cards.html',show_auth_buttons=True)

