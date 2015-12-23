import psycopg2
import select

from bentham.config import get_pg_db

BENTHAM_EVENTS_CHANNEL = 'bentham_events'


def main():
    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            pass
        else:
            conn.poll()
            while conn.notifies:
                print(conn.notifies.pop(0).payload)

if __name__ == '__main__':
    database = get_pg_db()
    conn = database.get_conn()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    curs = database.get_cursor()
    curs.execute('LISTEN %s' % BENTHAM_EVENTS_CHANNEL)

    main()
