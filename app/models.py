from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="student")
    type: so.Mapped[str] = so.mapped_column(sa.String(50))

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notifications = []

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# --- Student ---
@dataclass
class Student(User):
    __tablename__ = 'students'

    id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), primary_key=True)
    interests: so.Mapped[str] = so.mapped_column(sa.String(256))

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }

    def __repr__(self):
        return f'<Student {self.username}, interests={self.interests}>'

# --- Mentor ---
@dataclass
class Mentor(User):
    __tablename__ = 'mentors'

    id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), primary_key=True)
    expertise: so.Mapped[str] = so.mapped_column(sa.String(256))
    self_introduction: so.Mapped[str] = so.mapped_column(sa.Text)
    available_hours: so.Mapped[str] = so.mapped_column(sa.String(256))

    __mapper_args__ = {
        "polymorphic_identity": "mentor",
    }

    def __repr__(self):
        return f'<Mentor {self.username}, expertise={self.expertise}>'


# --- Admin ---
@dataclass
class Admin(User):
    __tablename__ = 'admins'

    id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

    def __repr__(self):
        return f'<Admin {self.username}>'

@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@dataclass
class Course(db.Model):
    __tablename__ = 'courses'

    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(255), nullable=False)
    platform: str = db.Column(db.String(100), nullable=False)
    difficulty: str = db.Column(db.String(50), nullable=False)
    subject: str = db.Column(db.String(100), nullable=False)
    url: str = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'<Course {self.title} ({self.platform})>'

# --- New Course Notification ---
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)


# # --- SavedCourses ---
# class SavedCourse(db.Model):
#     __tablename__ = 'saved_courses'
#
#     user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
#     course_id: int = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
#
#     user = db.relationship('User', backref=db.backref('saved_courses', lazy='dynamic'))
#     course = db.relationship('Course', backref=db.backref('saved_by', lazy='dynamic'))
#
#     def __repr__(self):
#         return f'<SavedCourse user_id={self.user_id} course_id={self.course_id}>'


@dataclass
class Mentor(db.Model):
    __tablename__ = 'mentors'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    subject: so.Mapped[str] = so.mapped_column(sa.String(64))
    description: so.Mapped[str] = so.mapped_column(sa.Text)

    def __repr__(self):
        return f'Mentor(id={self.id}, name={self.name},subject={self.subject} description={self.description})'

@dataclass #need to connect to forms
class Appointment(db.Model):
    __tablename__ = 'Appointments'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    mentor_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    topic: so.Mapped[str] = so.mapped_column(sa.String(64))
    message: so.Mapped[str] = so.mapped_column(sa.Text)

    def __repr__(self):
        return f'Appointment(id={self.id}, mentor_name={self.mentor_name},topic={self.topic},  message= {self. message})'

