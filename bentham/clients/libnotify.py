import notify2

notify2.init('Bentham')

def notify(event):
    notify2.Notification(event['message']).show()
