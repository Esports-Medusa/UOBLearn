from app.models import Notification, db

class StudentObserver:
    def __init__(self, student):
        self.student = student

    def update(self, message):
        notification = Notification(user_id=self.student.id, message=message)
        db.session.add(notification)