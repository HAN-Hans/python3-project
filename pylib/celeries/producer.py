import time

from celeries.tasks import add, dump_context


def add_task():
    start = time.time()
    task = add.delay(2, 3)
    while not task.ready():
        print('result not ready')
        print("task status:{0}".format(task.status))
        time.sleep(1)
    result = task.get()
    print(result)
    print('all time: {}'.format(time.time() - start))


if __name__ == '__main__':
    add_task()
