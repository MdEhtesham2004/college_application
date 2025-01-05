from flask import Flask,Blueprint, render_template,request,current_app,send_from_directory,redirect,url_for,Response,send_file,session,flash,jsonify
from flask_login import login_required,current_user
import requests 
import os 
from werkzeug.utils import secure_filename
import uuid
import time 
from werkzeug.security import generate_password_hash, check_password_hash
from . file import dump_messages,load_messages,load_community_messages,dump_community_message
from . job_search import get_jobs


main = Blueprint('main',__name__)



@main.route('/')
def index():
        show_auth_buttons = not current_user.is_authenticated
        return render_template('index.html',show_auth_buttons=show_auth_buttons,show_admin_functions=False)

@main.route('/home')
def home():
        show_auth_buttons = not current_user.is_authenticated
        return render_template('index.html',show_auth_buttons=show_auth_buttons,show_admin_functions=False)

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
    
    

@main.route("/account")
@login_required
def account():
     """  this function renders the user account page message from admin in messages and 
           jobs is the dictionary of the jobs_posting       """
     filepath="message.json"
     filepath_community="community_message.json"
     messages=load_messages(current_user.id,filepath)
     community_messages = load_community_messages(filepath_community)
     jobs = get_jobs()
     return render_template('account.html',messages=messages,jobs=jobs,community_messages=community_messages)

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
    default_img_path ='{{ url_for("static", filename="images_folder/default-img.png") }}'
    return render_template('account.html', default_img_path=default_img_path)
    # return redirect(url_for('static', filename='images_folder/default-img.png'))



@main.route("/opt_validation")
def otp():
    return render_template("otp_validation.html",show_email_input=True,
                           show_otp_input=False,
                           show_password_input=False)

from .mail import Mail
mail = Mail()
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
        return render_template(
                                "otp_validation.html",
                                show_email_input=False,
                                  show_otp_input=True,
                                    show_password_input=False
                                )



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
    
ADMIN_USERNAME="admin3133"
ADMIN_PASSWORD="MK_EHAN3133"

@main.route("/users")
def show_users():
    return render_template("users.html",show_admin_login=True ,show_user_details=False,show_auth_buttons=False,show_community_message=False,show_student_message=False)  


@main.route("/admin_authentication")
def admin_authenticaton():
    return render_template("adminAuthentication.html",show_admin_login=True)


@main.route("/validate_admin", methods=["POST"])
def validate_admin():
    admin = request.form.get("admin_id")
    password = request.form.get("admin_password")
    if admin == ADMIN_USERNAME and password ==ADMIN_PASSWORD:
        from . models import User
        users = User.query.all()
        return render_template("users.html", users=users, show_user_details=True,show_student_message=True,show_community_message=True,show_admin_auth=True)
    else:
        flash("Invalid credentials. Please try again.", "danger")
        return redirect(url_for("main.show_users"))
    




@main.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    from .models import  User 
    from . import db 
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
        return render_template("users.html",show_admin_login=False,show_user_details=True)  

    else:
        flash('User not found.', 'danger')
    return redirect(url_for('main.show_users',show_admin_login=True))

import json 

@main.route('/send_message', methods=['POST'])
def send_message():
    student_id = request.form.get('student_id')
    message = request.form.get('message')
    filepath = "message.json"
    dump_messages(int(student_id),message,filepath)
    
    from . models import User 
    student = User.query.get(student_id)
    if student:
        # Logic to send message to the student (e.g., save to database, send email, etc.)
        flash(f'Message sent to student ID {student_id} successfully!', 'success')
    else:
        flash(f'Student ID {student_id} not found.', 'danger')
    
    return redirect(url_for('main.show_users',show_admin_login=False,show_user_details=True,show_student_message=True,show_community_message=True))




@main.route('/show_students')
def show_students():
    return render_template("users.html",show_user_details=True,show_admin_login=False ,show_student_message=False,show_auth_buttons=False,show_admin_functions=True,show_community_message=False)  


@main.route('/remove_dp')
def remove_dp():
    from . import db 
    from .models import Image
    id = current_user.id
    try:
        # Step 1: Query the row to delete
        user_to_delete = Image.query.filter_by(user_id=id).first()
        
        # Step 2: Delete the row if it exists
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            print(f"User with id={user_to_delete.user_id} deleted successfully!")
            return redirect(url_for('main.account'))
        else:
            print(f"No image found for user with id={id}")

        # Redirect to the default image route
        # return redirect(url_for('main.get_default_img'))
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while removing the display picture.", 500
    


@main.route('/about')
def about():
    return render_template("about.html")


""" adding send community functionality   """

@main.route('/send_community_message',methods=['POST'])
def send_community_message():
    community_message = request.form.get('community_message')
    filepath = "community_message.json"
    dump_community_message(community_message,filepath)
    flash(f'Message sent to community successfully!', 'success')
    return redirect(url_for('main.show_users',show_admin_login=False,show_user_details=True,show_student_message=True,show_community_message=True))



