import time

import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
result = channel.queue_declare(exclusive=True)  # 创建一个临时的队列,用来接收消息,exclusive设为True当断开连接时删掉这个队列
queue_name = result.method.queue
channel.queue_bind(exchange='logs', queue=queue_name)  # 将队列绑定到路由上
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print("[x] Received %r" % body)
    # time.sleep(body.count(b'.'))
    # print("[x] Done")


# channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    callback,
    queue=queue_name,
    no_ack=True
)


channel.start_consuming()
