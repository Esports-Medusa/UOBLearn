from app import app, db
from models import User

with app.app_context():
    u1 = User(role='student', username='Alice', email='alice@example.com', is_first_login=False)
    u1.set_password('alice123')

    u2 = User(role='student', username='Bob', email='bob@example.com', is_first_login=False)
    u2.set_password('bob123')

    u3 = User(role='mentor', username='DrSmith', email='smith@example.com', is_first_login=True)
    u3.set_password('mentor123')

    db.session.add_all([u1, u2, u3])
    db.session.commit()

    print("✅ Demo users inserted.")
