import json
from twisted.internet import reactor
from txpostgres import txpostgres

BENTHAM_PG_NOTIFY_CHANNEL = 'bentham_events'

def observer(notify):
    print json.dumps(json.loads(notify.payload), indent=4)

if __name__ == '__main__':
    conn = txpostgres.Connection()
    d = conn.connect()

    conn.addNotifyObserver(observer)
    d.addCallback(lambda _: conn.runOperation('LISTEN %s' % BENTHAM_PG_NOTIFY_CHANNEL))

    reactor.run()
