from typing import Optional, List
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
    saved_courses = db.relationship("SavedCourse", back_populates="user", cascade="all, delete-orphan")

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
    meetings_sent: so.Mapped[List["Meeting"]] = db.relationship(
        "Meeting", back_populates="student", cascade="all, delete-orphan", lazy=True
    )


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
    meetings_received: so.Mapped[List["Meeting"]] = db.relationship(
        "Meeting", back_populates="mentor", cascade="all, delete-orphan", lazy=True
    )


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


# --- Meeting ---
@dataclass
class Meeting(db.Model):
    __tablename__ = 'meetings'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('students.id'), nullable=False)
    mentor_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('mentors.id'), nullable=False)
    meeting_time: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    status: so.Mapped[str] = so.mapped_column(sa.String(10), default='pending')  # 'pending', 'accepted', 'rejected'
    response_message: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.utcnow)
    is_viewed_by_student: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    # Relationships
    student = db.relationship("Student", back_populates="meetings_sent", lazy=True)
    mentor = db.relationship("Mentor", back_populates="meetings_received", lazy=True)

    def __repr__(self):
        return f'<Meeting {self.id} from Student {self.student_id} to Mentor {self.mentor_id}, status={self.status}>'




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


class SavedCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    type = db.Column(db.String(10))  # "saved" or "favourite"

    user = db.relationship("User", back_populates="saved_courses")
    course = db.relationship("Course")


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)