from app import db, app
from app.models import Student, Mentor, Admin

def load_students(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            name, username, email, password, interests = line.strip().split('|')
            student = Student(
                name=name,
                username=username,
                email=email,
                interests=interests,
                role='student'
            )
            student.set_password(password)
            db.session.add(student)

def load_mentors(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            name, username, email, password, expertise, intro, hours = line.strip().split('|')
            mentor = Mentor(
                name=name,
                username=username,
                email=email,
                expertise=expertise,
                self_introduction=intro,
                available_hours=hours,
                role='mentor'
            )
            mentor.set_password(password)
            db.session.add(mentor)

def load_admins(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            name, username, email, password = line.strip().split('|')
            admin = Admin(
                name=name,
                username=username,
                email=email,
                role='admin'
            )
            admin.set_password(password)
            db.session.add(admin)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        load_students('app/data/students.txt')
        load_mentors('app/data/mentors.txt')
        load_admins('app/data/admins.txt')
        db.session.commit()
        print("Users loaded successfully.")
