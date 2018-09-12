# RabbitMQ Hello World Tutorial

## 

```python
import sys
import pika


message = "".join(sys.argv[1:]) or "Hello World!"


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='hello')
channel.queue_declare(queue='task_queue', durable=True)  # 需要设置


# 向exchange扔任务,如果exchange为空默认会生成一个临时的
channel.basic_publish(
    exchange='',
    routing_key='hello',
    body=message
)

channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,
))



print("[X] Send %r" % message)


connection.close()

```