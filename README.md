# Kafka with Telegram

## Execution

1) Run your local zookeeper and kafka-broker:
```
bin/zookeeper-server-start.sh config/zookeeper.properties

bin/kafka-server-start.sh config/server.properties
```

2) Create a new cluster on https://bonsai.io
3) Change cluster url in ./elasticsearch_consumer.py in __init__()
4) Set a number of messages for producer more than 500 in ./start_producer.py
5) Run simultaneously ./start_consumer.py and ./start_consumer.py
6) To run faust use, where `kafka_streams` is a file name with your code
```
python -m faust -A kafka_streams worker -l info
```
7) Check your messages in topics with command
```
kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic telegram_messages7 --from-beginning
```