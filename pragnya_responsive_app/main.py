from flask import Flask,Blueprint, render_template,request,current_app,send_from_directory,redirect,url_for,Response,send_file,session,flash
from flask_login import login_required,current_user
import requests 
import os 
from werkzeug.utils import secure_filename
import uuid
import time 
from werkzeug.security import generate_password_hash, check_password_hash


main = Blueprint('main',__name__)



@main.route('/')
def index():
        show_auth_buttons = not current_user.is_authenticated
        return render_template('index.html',show_auth_buttons=show_auth_buttons)

@main.route('/home')
def home():
        show_auth_buttons = not current_user.is_authenticated
        return render_template('index.html',show_auth_buttons=show_auth_buttons)

@main.route('/mainpage/<username>')
@login_required
def mainpage(username):
    return render_template('cards.html',show_auth_buttons=False,username=username)

@main.route('/calculator')
def calculator():
    return render_template('calculator.html')

@main.route('/modelpaper')
def modelpaper():
    return render_template('model_paper.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('cards.html', username=current_user.name)


@main.route('/submit_grade', methods=['POST'])
def process_data():
    student_grade = request.form['my_js_var']  # Access the JavaScript variable from the form
    try:
        student_grade = float(student_grade)
        student_grade = round(student_grade, 2)  # Round to 2 decimal places
    except ValueError:
        return "Invalid grade input. Must be a number."  
    
    from .models import User 
    from . import db 
    
    email = current_user.email  
    student = User.query.filter_by(email=email).first()



    if student:
        # Update the grade for the existing user
        student.student_grade = student_grade
        db.session.commit()  # Commit the changes
        # return f"Grade updated for {student.name}."
        time.sleep(5)
        return redirect(url_for('main.profile'))
        # return render_template('calculator.html')
    
    else:
        return "User not found."
    
    # return f"Student Grade: {student_grade}"
    # print("Student grade is : ", student_grade)

# @main.route('/account')
# @login_required
# def account():
#     user_details = {
#         'id': current_user.id,
#         'username': current_user.name,
#         'email': current_user.email,
#         'student_grade' : current_user.student_grade,
#         'Profile_pic' : current_user.profile_pic,
#         # Add other attributes as needed
#     }
#     weather_condition = weather.get_weather()
#     return render_template('account.html', user=user_details, weather_condition=weather_condition)

@main.route("/account")
@login_required
def account():
     return render_template('account.html')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic', 'heif'}



@main.route('/courses')
def courses():
    return render_template('courses.html')


@main.route('/upload',methods=['POST'])
def upload():
    from .models import Image
    from . import db 
    pic = request.files['profile_pic']
    if not pic:
        # return redirect(url_for('static', filename='default_profile.jpg'))
        return "no pic uploaded ", 400 
    if pic:
        img_name = secure_filename(pic.filename)
        mimetype = pic.mimetype
        img_data = pic.read()  # Read the image binary data
        user_id = current_user.id  # Logged-in user ID

        

        existing_image = Image.query.filter_by(user_id=user_id).first()

        if existing_image:
            # Update the existing image record
            existing_image.img = img_data
            existing_image.imgname = img_name
            existing_image.mimetype = mimetype
            db.session.commit()  # Commit the changes to the database
            return "Image has been updated", 200 
        else:
            # Create a new image record for the user
            new_image = Image(user_id=user_id, img=img_data, imgname=img_name, mimetype=mimetype)
            db.session.add(new_image)
            db.session.commit()
            
    return "image has been uploaded ", 200 

     
@main.route("/image/<int:id>")
def get_img(id):
    from .models import Image
    from . import db 
    image = Image.query.filter_by(user_id=id).first()
    if not image or not image.img:
        default_img_path = 'static/images_folder/default-img.png'
        return redirect(url_for('static', filename='images_folder/default-img.png'))


    return Response(image.img,mimetype=image.mimetype)

     
    
    
    

@main.route('/uploads/<filename>', methods=['GET', 'POST'])
def display_image(filename):
    # Serve the file from the 'uploads' directory inside the project
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename)



@main.route('/default_img')
def get_default_img():
    default_img_path = 'static/images_folder/default-img.png'
    return redirect(url_for('static', filename='images_folder/default-img.png'))



@main.route("/opt_validation")
def otp():
    return render_template("otp_validation.html",show_email_input=True,
                           show_otp_input=False,
                           show_password_input=False)

from .mail import Mail
mail = Mail()

# show_email_input=True
@main.route("/send_otp",methods=["POST"])
def send_otp():
    user_mail = request.form['email_entered_reset_password']
    session['user_mail'] = user_mail
    otp = mail.send_token(user_mail)
    flash('OTP sent to your email successfully!', 'success')
    session['otp'] = otp
    return render_template(
                            "otp_validation.html",
                              show_email_input=False,
                                show_otp_input=True,
                                  show_password_input=False
                            )


@main.route("/validate_otp",methods=['POST'])
def validate_otp():
    entered_otp =int(request.form['otp'])
    if 'otp' in session and session['otp'] == int (entered_otp):
        flash('OTP validated successfully!', 'success')
        session.pop('otp', None)  # Clear the OTP from the session
        return render_template(
                                "otp_validation.html",
                                 show_email_input=False,
                                show_otp_input=False,
                                show_password_input=True
                                )
    else:
        flash('Invalid OTP. Please try again.', 'danger')
        print({f" failed otp {session.get('otp')}"})
        # return redirect(url_for('otp'))
        return render_template(
                                "otp_validation.html",
                                show_email_input=False,
                                  show_otp_input=True,
                                    show_password_input=False
                                )

# @main.route("/update_password", methods=["POST"])
# def update_password():
#     from . import db 
#     from . models import User

#     new_password = request.form['new_password']
#     confirm_password = request.form['confirm_password']
#     if new_password == confirm_password:
#         hashed_password = generate_password_hash(password=new_password,method='pbkdf2:sha256')
#         email = request.form['email']
#         user = User.query.filter_by(email=email).first()
#         if user:
#             user.password = hashed_password
#             db.session.commit()   
#         flash('Password updated successfully!', 'success')
#         # return render_template("otp_validation.html")
#         # current_user.password = new_password
#         return redirect(url_for('auth.login'))
#         # return "Success!"
#     else:
#         flash('Passwords do not match. Please try again.', 'danger')
#         # return redirect(url_for('otp'))
#         return render_template(
#                                 "otp_validation.html",
#                                   show_email_input=False,
#                                     show_otp_input=True,
#                                       show_password_input=True
#                                 )
    


@main.route("/update_password", methods=["POST"])
def update_password():
    from . import db 
    from . models import User
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    # email = request.form['email_entered_reset_pasword']  # Ensure email is retrieved correctly
    email = session.get('user_mail')  # Retrieve the email from the session
    print(f"Email from session: {email}")

    if not email:
        flash('Email is required to update the password.', 'danger')
        return render_template("otp_validation.html", show_email_input=False, show_otp_input=False, show_password_input=True)

    if new_password == confirm_password:
        hashed_password = generate_password_hash(password=new_password, method='pbkdf2:sha256')
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = hashed_password
            db.session.commit()
            flash('Password updated successfully!', 'success')
            session.pop('user_mail', None)  
            return redirect(url_for('auth.login'))
        else:
            flash('User not found.', 'danger')
            return render_template("otp_validation.html",
                                    show_email_input=True,
                                        show_otp_input=True,
                                        show_password_input=True)
    else:
        flash('Passwords do not match. Please try again.', 'danger')
        return render_template("otp_validation.html", 
                                show_email_input=False,
                                    show_otp_input=False,
                                    show_password_input=True)
    # except Exception as e:
    #     flash(f'An error occurred: {str(e)}', 'danger')
    #     return render_template("otp_validation.html", show_email_input=False, show_otp_input=False, show_password_input=True)