from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uoblearn.db'

db = SQLAlchemy(app)
login = LoginManager()
login.init_app(app)
login.login_view = 'auth.login'

migrate = Migrate(app, db)

from app.routes import auth, courses, mentor, main, register, meeting, saved_courses
app.register_blueprint(main.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(courses.bp)
app.register_blueprint(mentor.bp)
app.register_blueprint(register.bp)
app.register_blueprint(meeting.bp)
app.register_blueprint(saved_courses.bp)

__all__ = ['app', 'db', 'login']