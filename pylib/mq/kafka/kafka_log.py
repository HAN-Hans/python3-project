from kafka.client import KafkaClient
from kafka.producer import SimpleProducer, keyed
import logging
import traceback
import sys


class KafkaLoggingHandler(logging.Handler):
    pass