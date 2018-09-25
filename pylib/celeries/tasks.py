from celery import Celery, Task
from celery.utils.log import get_task_logger

from . import celeryconfig

app = Celery('tasks')
app.config_from_object(celeryconfig)
app.conf.setdefault('accept_content', ['application/json'])
print(app.conf.humanize(with_defaults=True, censored=True))
print(app.conf.table(with_defaults=False, censored=True))


logger = get_task_logger(__name__)


class DebugTask(Task):
    queue='base'
    def __call__(self, *args, **kwargs):
        logger.info('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)


# The app.task() decorators don’t create the tasks at the point when the task is defined,
# instead it’ll defer the creation of the task to happen either when the task is used,
# or after the application has been finalized, add.__evaluated__()
@app.task(bind=True, base=DebugTask)
def add(self, x, y):
    logger.info(self.name)
    return x + y


@app.task(bind=True, exchange='fanout')
def dump_context(self, x, y):
    logger.info('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(self.request))


if __name__ == '__main__':
    app.worker_main()
