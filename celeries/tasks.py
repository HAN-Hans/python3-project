from celery import Celery


app = Celery('tasks', broker='guest:guest://127.0.0.1:')


@app.task(bind=True)
def add(self, x, y):
    print(self.name)
    return x + y


@app.task(bind=True)
def dump_context(self, x, y):
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(self.request))


if __name__ == '__main__':
    app.worker_main()
