import configparser
from elasticsearch_consumer import TelegramConsumer


def start_consumer(topic, ip_address):
    consumer = TelegramConsumer(topic, ip_address)
    consumer.receive_messages()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Setting configuration values
    topic = config['Producer']['topic']
    ip_address = config['Producer']['ip_address']

    start_consumer(topic, ip_address)
