import ustruct
from umqtt.robust import MQTTClient
from machine import Pin
import network
import time
from umqtt.robust import MQTTClient
import sys
import os
import ujson
import urequests
from weight import HX711

def call_back_routine(feed, msg):
    print('Received Data:  feed = {}, Msg = {}'.format(feed, msg))
    if ADAFRUIT_IO_FEEDNAME2 in feed :
        action = str(msg, 'utf-8')
        if action == 'ON':
            pin2.value(0)
        elif action == 'OFF':
            pin2.value(1)
        print('action = {} '.format(action))
    if ADAFRUIT_IO_FEEDNAME3 in feed:
        a = int(str(msg, 'utf-8'))
        threshold_notify.append(a)
        print('threshold={}'.format(threshold_notify))
    if ADAFRUIT_IO_FEEDNAME4 in feed:
        a = int(str(msg, 'utf-8'))
        threshold_water.append(a)
        print('threshold={}'.format(a))

ADAFRUIT_IO_URL = b'io.adafruit.com'
ADAFRUIT_USERNAME = b'Username here'
ADAFRUIT_IO_KEY = b'adafruit IO key here'
ADAFRUIT_IO_FEEDNAME1 = b'temperature'
ADAFRUIT_IO_FEEDNAME2 = b'weight'

ADAFRUIT_IO_FEEDNAME4 = b'threshold_water'
def Send_Data(tTemp) :
    client.publish(mqtt_feedname1,bytes(str(tTemp), 'utf-8'), qos=0)
def Send_weight_data(val):
    client.publish(mqtt_feedname2, bytes(str(val), 'utf-8'), qos=0)
threshold_notify = [400]
threshold_water = [230]

# create a random MQTT clientID
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')


client = MQTTClient(client_id=mqtt_client_id,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)

#ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME1
mqtt_feedname1 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME1), 'utf-8')
mqtt_feedname2 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME2), 'utf-8')
mqtt_feedname4 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME4), 'utf-8')

class SensorBase:

    def read16(self, register):
        data = self.i2c.readfrom_mem(self.address, register, 2)
        return ustruct.unpack('<H', data)[0]

    def read_temp(self, register):
        temp = self.read16(register);
        # apply measurement resolution (0.02 degrees per LSB)
        temp *= .02;
        # Kelvin to Celcius
        temp -= 273.15;
        return temp;

    def read_ambient_temp(self):
        return self.read_temp(self._REGISTER_TA)

    def read_object_temp(self):
        return self.read_temp(self._REGISTER_TOBJ1)

    def read_object2_temp(self):
        if self.dual_zone:
            return self.read_temp(self._REGISTER_TOBJ2)
        else:
            raise RuntimeError("Device only has one thermopile")

    @property
    def ambient_temp(self):
        return self.read_ambient_temp()

    @property
    def object_temp(self):
        return self.read_object_temp()

    @property
    def object2_temp(self):
        return self.read_object2_temp()


class MLX90614(SensorBase):
    _REGISTER_TA = 0x06
    _REGISTER_TOBJ1 = 0x07
    _REGISTER_TOBJ2 = 0x08

    def __init__(self, i2c, address=0x5a):
        self.i2c = i2c
        self.address = address
        _config1 = i2c.readfrom_mem(address, 0x25, 2)
        _dz = ustruct.unpack('<H', _config1)[0] & (1 << 6)
        self.dual_zone = True if _dz else False


class MLX90615(SensorBase):
    _REGISTER_TA = 0x26
    _REGISTER_TOBJ1 = 0x27

    def __init__(self, i2c, address=0x5b):
        self.i2c = i2c
        self.address = address
        self.dual_zone = False


import time
from machine import I2C, Pin
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ssid', 'password')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    try:
        client.connect()
    except Exception as e:
        print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
        sys.exit()
i2c = I2C(scl=Pin(5), sda=Pin(4))
sensor = MLX90614(i2c)
wlan = wm.get_connection()
    if wlan is None:
        print("Could not initialize the network connection.")
        while True:
            pass  # you shall not pass :D
    try:
        client.connect()
    except Exception as e:
        print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
        sys.exit()
while True:
    print(sensor.read_ambient_temp(), sensor.read_object_temp())
    Send_Data(sensor.read_object_temp())
    time.sleep_ms(500)
    hx = HX711(5, 4)
    hx.tare()
    val = hx.read()
    val = hx.get_value()
    Send_weight_data(val)

