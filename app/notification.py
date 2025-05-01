class NotificationCenter:
    def __init__(self):
        self.observers = []

    def register_observer(self, user):
        if user not in self.observers:
            self.observers.append(user)

    def notify_all(self, message):
        for user in self.observers:
            if hasattr(user, "notifications"):
                user.notifications.append(message)