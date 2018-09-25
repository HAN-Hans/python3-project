import json
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('ascii'),
    key_serializer=lambda m: json.dumps(m).encode('ascii'),
    compression_type='gzip',
)
future = producer.send(
    'contry', 
    key={'china': 1},
    value={'beijing': 1},
    partition=0,
)
result = future.get(timeout=10)
print(result)
