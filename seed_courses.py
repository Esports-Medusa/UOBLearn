from app import db, app
from app.models import Course

def load_courses(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 5:
                title, platform, difficulty, subject, url = parts
                course = Course(
                    title=title,
                    platform=platform,
                    difficulty=difficulty,
                    subject=subject,
                    url=url
                )
                db.session.add(course)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        load_courses('app/data/courses.txt')
        db.session.commit()
        print("Courses loaded successfully.")
