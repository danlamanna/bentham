from bentham import configObject
from bentham.constants import BENTHAM_EVENTS_CHANNEL

import pgpubsub


def listener():
    cfg = configObject.load()
    pubsub = pgpubsub.connect(cfg['datastore']['uri'])
    pubsub.listen(BENTHAM_EVENTS_CHANNEL)

    return pubsub
