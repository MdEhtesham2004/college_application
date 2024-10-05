from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from flask_migrate import Migrate


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'clg_application'  # Replace with a strong, unique key


    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    
    login_manager.init_app(app=app)
    login_manager.login_view = 'auth.login'  # Set this to your login view endpoint

    
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications    
    
    UPLOAD_FOLDER = '/pragnya_responsive_app/static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))



    from .models import db
    migrate = Migrate(app, db)

    db.init_app(app=app)
    with app.app_context():
        db.create_all()  # Creates the database tables
    


    return app


