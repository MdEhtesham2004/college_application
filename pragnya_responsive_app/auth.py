from flask import Blueprint, render_template, redirect, url_for, request, flash,session,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required,current_user
from . mail import Mail
import time

auth = Blueprint('auth', __name__)


@auth.route('/login_post',methods=['GET','POST'])
def login_post():
    if request.method == 'POST':
        email = request.form['email_login']
        password = request.form['password_login']
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
        

NAME=""
EMAIL=""
PASSWORD=""


@auth.route('/signup_post', methods=['GET', 'POST'])
def signup_post():
    global otp_validation 
    global NAME 
    global EMAIL
    global PASSWORD
    if request.method == 'POST':
        fname = request.form['firstName']
        lname = request.form['lastName']
        name = fname + ' ' + lname
        NAME=name
        email = request.form["email"]
        EMAIL = email
        password = request.form["password"]
        confirm_password = request.form["confirmPassword"]
        hashed_password = generate_password_hash(password=password,method='pbkdf2:sha256')
        PASSWORD=hashed_password
        
        if password != confirm_password:
            flash("Passwords don't match", "error")
            return redirect(url_for("auth.signup"))
        





        from .models import User
        from . import db 
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash(f"User with {email} already exits!")
            return render_template("signUp.htm")
        



        mail = Mail()
        otp =  mail.send_token(email)
        if otp: 
            session['otp'] = otp
            session['user_mail'] = email
            print(f"otp in session: {session.get('otp')}")
            flash('OTP sent to your email successfully!', 'success')
            return render_template('signUp.htm', show_signup_fields=False,show_otp_input=True)
        
        


        if otp_validation:
            new_user = User(name=name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Signup Successful!", 'success')
            return redirect(url_for("auth.login"))
        else:
            flash("OTP validation failed. Please try again.", "error")
            return redirect(url_for("auth.signup"))
    
    # Handle GET request: render the signup page
    return render_template('signUp.htm')

otp_validation = ""


@auth.route("/validate_otp_signup",methods=['POST'])
def validate_otp_signup():
    global NAME
    global EMAIL
    global PASSWORD
    from . import db 
    from . models import User 
    global otp_validation
    entered_otp =int(request.form['otp_signup'])
    print(f"Entered OTP: {entered_otp}")
    if 'otp' in session and session.get('otp') == int (entered_otp):
        flash('OTP validated successfully!', 'success')
        session.pop('otp', None)  # Clear the OTP from the session
        otp_validation = True
        # return True
        new_user = User(name=NAME, email=EMAIL, password=PASSWORD)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup Successful!", 'success')
        return redirect(url_for("auth.login"))
    else:
        flash('Invalid OTP. Please try again.', 'danger')
        print({f" failed otp {session.get('otp')}"})
        otp_validation = False
        return redirect(url_for(auth.signup))

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
    return render_template('signUp.htm',show_auth_buttons=True,show_signup_fields=True,show_otp_input=False)

@auth.route('/Account')
@login_required
def Account():
    return render_template('cards.html',show_auth_buttons=True)

@auth.route('/About')
@login_required
def About():
    return render_template('about.html',show_auth_buttons=True)





















