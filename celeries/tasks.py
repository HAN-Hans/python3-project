from celery import Celery


app = Celery()


@app.task(bind=True)
def add(self, x, y):
    print(self.name)
    return x + y

if __name__ == '__main__':
    app.worker_main()