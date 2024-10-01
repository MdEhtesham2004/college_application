from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet
from flask_cors import CORS


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'clg_application'  # Replace with a strong, unique key
    CORS(app, resources={r"/*": {"origins": "*"}})

    # socketio = SocketIO(app)

    socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for SocketIO


    # socketio = SocketIO(app)


    # socketio.run(app, host='0.0.0.0', port=5000, debug=True, server='eventlet')



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

    # Socket Events
    @socketio.on('join')
    def on_join(data):
        username = data['username']
        room = data['room']
        join_room(room)
        emit('message', {'msg': f"{username} has joined the room."}, room=room)

    @socketio.on('message')
    def handle_message(data):
        room = data['room']
        emit('message', {'msg': f"{data['username']}: {data['msg']}"}, room=room)

    @socketio.on('leave')
    def on_leave(data):
        username = data['username']
        room = data['room']
        leave_room(room)
        emit('message', {'msg': f"{username} has left the room."}, room=room)
    


    from .models import db
    migrate = Migrate(app, db)

    db.init_app(app=app)
    with app.app_context():
        db.create_all()  # Creates the database tables
    


    return app,socketio


