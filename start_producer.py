import os
import logging
import telethon
import configparser

from producer import TelegramMessageProducer
from collect_data.download_dialogs_data import download_dialog
from collect_data.utils import init_config, read_dialogs


if __name__ == '__main__':
    tg_producer = TelegramMessageProducer()
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Setting configuration values
    topic = config['Producer']['topic']
    ip_address = config['Producer']['ip_address']

    CONFIG_PATH = os.path.join('collect_data', 'config_collect_data.json')
    MSG_LIMIT = 500
    SESSION_NAME = 'session1'
    DEBUG_MODE = True
    DIALOGS_IDS = [138918380, 347963763, 391370223]

    config = init_config(CONFIG_PATH)
    dialogs_list = read_dialogs(config["dialogs_list_folder"])
    client = telethon.TelegramClient(SESSION_NAME, config["api_id"], config["api_hash"])

    if DEBUG_MODE:
        logging.basicConfig(level=logging.DEBUG)

    for id in DIALOGS_IDS:
        print(f"Loading dialog #{id}")

        with client:
            client.loop.run_until_complete(download_dialog(client, id, MSG_LIMIT, tg_producer, topic))
