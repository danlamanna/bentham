import notify2
from bentham.clients.basic import Client

notify2.init('Bentham')


class LibnotifyClient(Client):
    def emit(self, event):
        notify2.Notification(self.get_message(event)).show()


__client__ = LibnotifyClient
