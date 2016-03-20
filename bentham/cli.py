from bentham import configObject
from bentham.database import events
from bentham.listener import listener
from bentham.utils import bentham_checkin

import click
import datetime as dt
import importlib
import json
import socket
import sys


@click.group()
def cli():
    pass


@cli.command()
@click.argument('tracker')
@click.argument('source')
def track(tracker, source):
    try:
        tracker_module = importlib.import_module('bentham.trackers.%s' % tracker)
        tracker_func = getattr(tracker_module, 'track')
    except ImportError:
        click.secho('Unable to find tracker bentham.trackers.%s' % tracker, err=True, fg='red')
        sys.exit(1)
    except AttributeError:
        click.secho('Tracker bentham.trackers.%s has no track function' % tracker, err=True, fg='red')
        sys.exit(1)

    db, cfg = (configObject.get_pg_db(),
               configObject.load('trackers', tracker + '.yml')[source],)

    tracker_func(source, db, cfg)
    bentham_checkin(tracker, source, db, cfg)


@cli.command()
@click.argument('client_name')
def client(client_name):
    """
    Invoke a Bentham client.

    This will start the Bentham client passed as CLIENT_NAME, by default it will use
    the 'basic' client which is included with Bentham - this simply prints the JSON
    dump of the event as it occurs using the LISTEN/NOTIFY facilities built into
    PostgreSQL.
    """
    try:
        client_module = importlib.import_module('bentham.clients.%s' % client_name)
        client_func = getattr(client_module, 'notify')
    except ImportError:
        click.secho('Unable to find client bentham.clients.%s' % client_name, err=True, fg='red')
        sys.exit(1)
    except AttributeError:
        click.secho('Client bentham.clients.%s has no listen function' % tracker, err=True, fg='red')
        sys.exit(1)


    for event in listener().events():
        client_func(json.loads(event.payload))


@cli.command()
@click.argument('message')
def log(message):
    db = configObject.get_pg_db()
    db.execute(events.insert(),
               occurred_at=dt.datetime.utcnow(),
               tracker='cli',
               source=socket.gethostname(),
               message=message)
