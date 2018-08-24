import sys
import pika


message = "".join(sys.argv[1:]) or "Hello World!"


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
result = channel.queue_declare(exclusive=True)
channel.queue_bind(exchange='logs', queue=result.method.queue)


channel.basic_publish(
    exchange='logs',
    routing_key='',
    body=message,
)


print("[X] Send %r" % message)


connection.close()
