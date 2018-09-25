import sys
import pika


message = "".join(sys.argv[1:]) or "Hello World!"


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)  # durable设置为True,即使rabbitmq重启也队列也不会消失


channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
      delivery_mode=2,  # 将消息设置为持久化
))


print("[X] Send %r" % message)


connection.close()
