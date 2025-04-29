from tkinter.font import names

from app.models import User, Course, Mentor

def reset_db():
    from app import db
    db.drop_all()
    db.create_all()

    u1 = User(username='amy', email='a@b.com', role='Admin')
    u1.set_password('amy.pw')
    u2 = User(username='tom', email='t@b.com')
    u2.set_password('tom.pw')
    u3 = User(username='yin', email='y@b.com', role='Admin')
    u3.set_password('yin.pw')
    u4 = User(username='tariq', email='tariq@b.com')
    u4.set_password('tariq.pw')
    u5 = User(username='jo', email='jo@b.com')
    u5.set_password('jo.pw')

    db.session.add_all([u1, u2, u3, u4, u5])


    m1 = Mentor(name="Jane", subject='cloud computing', description="hello i love cloud computing")
    m2 = Mentor(name="Alex", subject="Machine Learning", description="I'm passionate about building smart systems that learn.")
    m3 = Mentor(name="Sanjay", subject="Cybersecurity", description="Security is key to everything. I enjoy ethical hacking and protecting data.")
    m4 = Mentor(name="Maria", subject="Data Science", description="I love discovering insights from data and solving problems with it.")
    m5 = Mentor(name="Liam", subject="Web Development",description="I specialize in building fast, responsive web apps using modern tech.")

    db.session.add_all([m1, m2, m3, m4, m5])


    db.session.commit()
