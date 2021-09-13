import configparser
import faust


config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
topic = config['Producer']['topic']
ip_address = config['Producer']['ip_address']


app = faust.App('telegram-messages-stream', broker=ip_address)
topic_obj = app.topic(topic)
important_topic_obj = app.topic('important_' + topic)


@app.agent(topic_obj)
async def filter_messages(records):
    async for record in records:
        if record['id'] > 154_000:
            print("record['id'] -- ", record['id'])
            await important_topic_obj.send(value=record)


if __name__ == '__main__':
    app.main()
