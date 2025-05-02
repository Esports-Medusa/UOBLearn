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

from app.routes import auth, courses, mentor, main
app.register_blueprint(main.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(courses.bp)
app.register_blueprint(mentor.bp)

__all__ = ['app', 'db', 'login']

@app.shell_context_processor
def make_shell_context():
    return dict(db=db)
