from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    preferences = db.Column(db.String(500)) # Save user preference keywords (e.g., in JSON format)
    is_first_login = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    platform = db.Column(db.String(50))  # coursera, edx, ...
    description = db.Column(db.Text)
    keywords = db.Column(db.String(300))
    url = db.Column(db.String(300))
    # for ML
    external_id = db.Column(db.String(50))  # e.g. coursera slug
    tags = db.Column(db.String(200))  # used for TF-IDF etc.
