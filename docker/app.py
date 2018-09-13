from flask import Flask
from redis import Redis, RedisError
import os
import socket

<<<<<<< HEAD

# Connect to Redis
redis = Redis(host="127.0.0.1", port=6379, db=0, socket_connect_timeout=2, socket_timeout=2)
=======
# Connect to Redis
redis = Redis(host="127.0.0.1", db=0, socket_connect_timeout=2, socket_timeout=2)
>>>>>>> celery

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
<<<<<<< HEAD
    app.run(host='0.0.0.0', port=80)
=======
    app.run(port=4000)
>>>>>>> celery
