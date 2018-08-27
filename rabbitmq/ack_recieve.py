import time

import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print("[x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print("[x] Done")
    print(method.delivery_tag)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 在回调函数中作响应


# 发生这种情况是因为RabbitMQ只是在消息进入队列时调度消息,它不会查看消费者未确认消息的数量
# 它只是盲目地向第n个消费者发送每个第n个消息
channel.basic_qos(prefetch_count=1)  # worker每次取一个消息

channel.basic_consume(
    callback,
    queue='task_queue',
    no_ack=False  # 自动消息响应关闭,需要在worker中作响应,如果没有的话消息会处于unacked
)


channel.start_consuming()
