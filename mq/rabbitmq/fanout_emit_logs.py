import sys
import pika


message = "".join(sys.argv[1:]) or "Hello World!"


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')


channel.basic_publish(
    exchange='logs',
    routing_key='',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2
    )
)


print("[X] Send %r" % message)


connection.close()
