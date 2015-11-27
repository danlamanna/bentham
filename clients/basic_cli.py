import requests
from time import sleep

CLIENT_INTERVAL = 60
SERVER_URL = 'http://127.0.0.1:8080/api/logs'

def handler(event):
    print 'Got an event, %d' % int(event['id'])

if __name__ == '__main__':
    since_id = 0

    while True:
        print 'Checking for events...'

        r = requests.get(SERVER_URL, params={'since_id': since_id})

        if r.ok and r.json()['data'] and r.json()['success']:
            data = r.json()['data']
            since_id = max([e['id'] for e in data])

            map(handler, data)

        sleep(CLIENT_INTERVAL)
