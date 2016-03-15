from bentham.constants import BENTHAM_EVENTS_CHANNEL

import psycopg2
import select


def listen(db):
    def poll():
        while True:
            if select.select([db.connection], [], [], 5) == ([], [], []):
                pass
            else:
                db.connection.poll()
                while db.connection.notifies:
                    print(db.connection.notifies.pop(0).payload)

    db.execution_options(autocommit=True)
    db.execute('LISTEN %s' % BENTHAM_EVENTS_CHANNEL)

    poll()
