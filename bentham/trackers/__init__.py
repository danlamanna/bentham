from __future__ import absolute_import

from celery import Celery

app = Celery('bentham',
             broker='amqp://rabbit:rabbit@rabbit',
             backend='amqp://rabbit:rabbit@rabbit',
             include=['bentham.trackers.fib'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_SEND_EVENTS=True,
    CELERY_SEND_TASK_SENT_EVENT=True
)

if __name__ == '__main__':
    app.start()
