from bentham.utils import get_tracker_config
import importlib


class Client():

    def __init__(self):
        pass

    @staticmethod
    def get_message(event):
        tracker = event['tracker']
        cfg = get_tracker_config(tracker, event['source'])

        tracker_module = importlib.import_module('bentham.trackers.%s' % tracker)
        receive_func = getattr(tracker_module, 'receive')

        return receive_func(event, cfg)

    def emit(self, event):
        print(self.get_message(event))


__client__ = Client
