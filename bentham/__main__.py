import cherrypy
import json
from playhouse.shortcuts import model_to_dict
from database import Event, db


class Events(object):
    exposed = True

    def GET(self, since_id=0):
        logs = Event.select() \
                  .where(Event.id > since_id) \
                  .order_by(Event.occurred_at.desc(),
                            Event.created_at.desc())

        for log in logs:
            log.created_at = str(log.created_at)
            log.occurred_at = str(log.occurred_at)

        logs = [model_to_dict(l) for l in logs]

        return json.dumps({"success": True,
                           "data": logs})

    @cherrypy.tools.json_in()
    def PUT(self):
        body = cherrypy.request.json
        if 'raw' not in body:
            body['raw'] = ''

        if 'raw_json' not in body:
            body['raw_json'] = {}

        try:
            Event(**body).save()
        except:
            # Event error
            db.rollback()
            return json.dumps({"success": False})
        finally:
            return json.dumps({"success": True})

if __name__ == '__main__':
    cherrypy.tree.mount(
        Events(), '/api/logs',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )

    cherrypy.engine.start()
    cherrypy.engine.block()
