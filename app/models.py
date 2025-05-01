from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass


@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)  # ✅ 新增真实姓名字段
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="student")
    type: so.Mapped[str] = so.mapped_column(sa.String(50))
    saved_courses = db.relationship('Course', secondary='saved_courses', back_populates='saved_by_users')

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type
    }

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
    saved_by_user = db.relationship('User', secondary='saved_courses', back_populates='saved_courses')

    def __repr__(self):
        return f'<Course {self.title} ({self.platform})>'


# --- SavedCourses ---
class SavedCourse(db.Model):
    __tablename__ = 'saved_courses'

    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    course_id: int = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)

    user = db.relationship('User', backref=db.backref('saved_courses', lazy='dynamic'))
    course = db.relationship('Course', backref=db.backref('saved_by', lazy='dynamic'))

    def __repr__(self):
        return f'<SavedCourse user_id={self.user_id} course_id={self.course_id}>'
