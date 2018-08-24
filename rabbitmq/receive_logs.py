import time

import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='logs', queue=queue_name)
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
