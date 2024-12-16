from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    student_grade = db.Column(db.Float, nullable=True)  # Float for grades

    # Relationship to Image table (one-to-many relationship)
    images = db.relationship('Image', backref='user', lazy=True)

class Image(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)  # Foreign key reference to the User table
    img = db.Column(db.LargeBinary, nullable=False)  # Storing image data as binary
    imgname = db.Column(db.String(200), nullable=True)  # Name of the image file
    mimetype = db.Column(db.String(100), nullable=True)  # Mime type of the image

    def __repr__(self):
        return f'<Image {self.imgname}>'
