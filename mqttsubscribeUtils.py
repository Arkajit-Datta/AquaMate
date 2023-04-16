import paho.mqtt.client as mqtt
from Adafruit_IO import MQTTClient

# Set up the Adafruit IO client
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'
ADAFRUIT_IO_KEY = 'YOUR_AIO_MQTT_API_KEY'
ADAFRUIT_IO_FEED = 'YOUR_AIO_FEED_NAME'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(ADAFRUIT_IO_FEED)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

aio_client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
aio_client.on_connect = on_connect
aio_client.on_message = on_message
aio_client.connect()
