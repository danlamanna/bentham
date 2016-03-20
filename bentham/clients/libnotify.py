import notify2

notify2.init('Bentham')

def notify(self, message, event):
    notify2.Notification(message).show()
