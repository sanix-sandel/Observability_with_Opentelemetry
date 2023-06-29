#! /usr/bin/env python3
import json
import threading

from confluent_kafka import Consumer
from flask import Flask

from common import kafka_topic, kafka_bootstrap_servers

app = Flask(__name__)


consumer = Consumer({
    'bootstrap.servers': kafka_bootstrap_servers,
    'auto.offset.reset': 'earliest',
    'group.id': '1'
})


def consume_event():
    consumer.subscribe([kafka_topic])
    while True:
        event = consumer.poll(5.0)
        if event is None:
            continue
        data = json.loads(event.value())
        print(data)


consumer_thread = threading.Thread(target=consume_event)
consumer_thread.start()


if __name__ == '__main__':
    app.run(debug=True, port=5002)