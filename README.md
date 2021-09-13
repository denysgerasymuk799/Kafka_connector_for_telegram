# Kafka with Telegram

## Execution

1) Run your local zookeeper and kafka-broker:
```
bin/zookeeper-server-start.sh config/zookeeper.properties

bin/kafka-server-start.sh config/server.properties
```

2) Change your credits in config.ini and ./collect_data/config_collect_data.json. ip_address is an ip of your zookeeper.
3) Create a new cluster on https://bonsai.io
4) Change cluster url in ./elasticsearch_consumer.py in __init__()
5) Set a number of messages for producer more than 500 in ./start_producer.py
6) Run simultaneously ./start_consumer.py and ./start_consumer.py
7) To run faust use this command, where `kafka_streams` is a file name with your code without file format .py
```
python -m faust -A kafka_streams worker -l info
```
7) Check your messages in topics with command
```
kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic telegram_messages7 --from-beginning
```