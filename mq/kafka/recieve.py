import json
from kafka import KafkaConsumer, TopicPartition


consumer = KafkaConsumer(
    # 'contry', # topic name
    group_id='group_2', 
    bootstrap_servers=['localhost:9092'],
    # consumer_timeout_ms=1000,
    value_deserializer=lambda m: json.loads(m.decode('ascii')),
    key_deserializer=lambda m: json.loads(m.decode('ascii')),
)
# consumer.assign([TopicPartition(topic='contry', partition=0)])
# consumer.subscribe(pattern='^my.*')
consumer.subscribe(topics=['streams-plaintext-input', 'contry'])

for msg in consumer:
    print(msg)
