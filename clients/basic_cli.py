import select
import psycopg2
import psycopg2.extensions

BENTHAM_EVENTS_CHANNEL = 'bentham_events'


def main():
    while True:
        if select.select([conn],[],[],5) == ([],[],[]):
            pass
        else:
            conn.poll()
            while conn.notifies:
                print(conn.notifies.pop(0).payload)

if __name__ == '__main__':
    conn = psycopg2.connect(database='bentham',
                            user='bentham',
                            password='bentham',
                            host='192.168.13.37')
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    curs = conn.cursor()
    curs.execute('LISTEN %s' % BENTHAM_EVENTS_CHANNEL)

    main()
