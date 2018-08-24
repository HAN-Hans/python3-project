import sys
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')


severity = sys.argv[1] if len(sys.argv) >= 2 else 'info'
message = " ".join(sys.argv[2:]) or "Hello World!"
channel.basic_publish(
    exchange='topic_logs',
    routing_key=severity,
    body=message,
)


print("[X] Send %r:%r" % (severity, message))
connection.close()
