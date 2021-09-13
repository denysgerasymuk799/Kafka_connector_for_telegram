import logging.config
import time
import uuid

from json import loads
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch, helpers

import custom_logger

logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(custom_logger.MyHandler())


class TelegramConsumer:
    def __init__(self, topic, ip_address):
        self.__es_client = Elasticsearch(
            ["https://bed4hpypg0:p6r6ozzfff@kafka-stream-cluster-679975384.eu-central-1.bonsaisearch.net:443"])

        self.consume_topic = topic
        self.__consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[ip_address],
            auto_offset_reset='latest',
            enable_auto_commit=False,
            group_id='tg_consumers1',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            max_poll_records=10
        )
        self.__consumer.subscribe([topic])

        if not self.__es_client.exists(topic, "0"):
            self.__es_client.indices.create(index=topic, ignore=400)
            res = self.__es_client.index(index=self.consume_topic,
                                         id="0",
                                         body={"doc": "first document in index"})
            logger.info(f"Consumer: Added first document in index, res -- {res}")

    def receive_messages(self):
        while True:
            dict_records = self.__consumer.poll(100)
            logger.info("Consumer: Received new package of messages")
            print("dict_records -- ", dict_records)

            for records in dict_records.values():
                if len(records) > 0:
                    # response = helpers.bulk(self.__es_client, records, index=self.consume_topic, doc_type="_doc")
                    response = helpers.bulk(self.__es_client, self.bulk_json_data(records))

                    logger.info(f"receive_messages(): Response -- {response}")
                    logger.info("Committing offsets...")
                    self.__consumer.commit()
                    logger.info("Offsets have been committed")

                    time.sleep(1)

    def bulk_json_data(self, records):
        for record in records:
            print("record.value -- ", record.value)

            if '{"index"' not in record:
                yield {
                    "_index": self.consume_topic,
                    "_type": "_doc",
                    "_source": record.value
                }
