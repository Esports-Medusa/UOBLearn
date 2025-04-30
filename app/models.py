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
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="Normal")

    def __repr__(self):
        pwh = 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
