import paho.mqtt.client as mqtt
from Adafruit_IO import MQTTClient


class AquamateAdafruit:
    def __init__(self) -> None:
        # Set up the Adafruit IO client
        self.ADAFRUIT_IO_USERNAME = 'Anirudh_Chebolu'
        self.ADAFRUIT_IO_KEY = 'aio_Qrhf15VIZUZoOku53qFZAexKGYha'
        self.aio_client = self.load()
        
    def on_connect(self,client, userdata, flags, rc):
        print(f"Connected with result code {str(rc)}")
        client.subscribe(self.ADAFRUIT_IO_FEED)

    def on_message(self, client, userdata, msg):
        print(f"{msg.topic} {str(msg.payload)}")

    def load(self):
        aio_client = MQTTClient(self.ADAFRUIT_IO_USERNAME, self.ADAFRUIT_IO_KEY)
        aio_client.on_connect = self.on_connect
        aio_client.on_message = self.on_message
        aio_client.connect()
        return aio_client

    def publish_message(self, feed_name, value):
        # Publish a message to Adafruit IO
        self.aio_client.publish(feed_name, value)
