from flask import Flask,Blueprint, render_template,request,current_app,send_from_directory,redirect,url_for,Response
from flask_login import login_required,current_user
import requests 
import os 
from werkzeug.utils import secure_filename
import uuid
import time 
from .apis import WeatherReport

weather = WeatherReport()

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

# Function to check allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

FILEPATH = ""

# @main.route('/upload', methods=['POST'])
# def upload_file():
#     if 'profile_pic' not in request.files:
#         return "No file part"
    
#     file = request.files['profile_pic']
    
#     if file.filename == '':
#         return "No selected file"
    
    
#     upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
#     if not os.path.exists(upload_folder):
#         os.makedirs(upload_folder)
    
    
#     if file and allowed_file(file.filename):
#         filename =  secure_filename(file.filename)
#         file_path = os.path.join(upload_folder, filename)
#         file.save(file_path)
   
#     from .models import User 
#     from . import db 
        
            
#     email = current_user.email  
#     user = User.query.filter_by(email=email).first()

#     if user:
#         # Update the grade for the existing user
#         user.profile_pic=filename
#         db.session.commit()  # Commit the changes
#         # image_url = url_for('', filename=user.image_path.split('pragnya_responsive_app/')[1])
#         image_url = user.profile_pic        
#         # return redirect(url_for('main.display_image', filename=filename))
#         # return render_template('accounts.html', filename=filename)
#         return render_template('account.html', filename=image_url)
    
#     else:
#         return 'Invalid file format'



@main.route('/upload',methods=['POST'])
def upload():
    from .models import Image
    from . import db 
    pic = request.files['profile_pic']
    if not pic:
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

    # img = Image(img=pic.read(),mimetype=mimetype,imgname=filename)

 
    # db.session.add(img)
    # db.session.commit()

    return "image has been uploaded ", 200 

     
@main.route("/<int:id>")
def get_img(id):
    from .models import Image
    from . import db 
    image = Image.query.filter_by(user_id=id).first()
    if not image:
        return f"no image with {id} as  id ", 404

    return Response(image.img,mimetype=image.mimetype)

     
    
    
    

@main.route('/uploads/<filename>', methods=['GET', 'POST'])
def display_image(filename):
    # Serve the file from the 'uploads' directory inside the project
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename)





