# https://learn.adafruit.com/mqtt-in-circuitpython/circuitpython-wifi-usage
# https://learn.adafruit.com/mqtt-in-circuitpython/connecting-to-a-mqtt-broker
# required from adafruit_bundle:
# - adafruit_requests
# - adafruit_minimqtt
import time
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import board
import touchio
import adafruit_dotstar
import feathers2
import alarm

feathers2.enable_LDO2(True)
dotstar = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.05, auto_write=True)


# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials. DO NOT share that file or commit it into Git or other
# source control.
# pylint: disable=no-name-in-module,wrong-import-order
def dotstar_error():
    dotstar[0] = (0,0,0)
    times = 0
    while times < 10:
        dotstar[0] = (255,0,0)
        time.sleep(0.05)
        dotstar[0] = (0,0,0)
        time.sleep(0.05)
        times += 1

def dotstar_wifi_success():
    dotstar[0] = (0,0,0)
    times = 0
    while times < 10:
        dotstar[0] = (0,255,0)
        time.sleep(0.05)
        dotstar[0] = (0,0,0)
        time.sleep(0.05)
        times += 1

def dotstar_mqtt_success():
    dotstar[0] = (0,0,0)
    times = 0
    while times < 10:
        dotstar[0] = (0,255,0)
        time.sleep(0.05)
        dotstar[0] = (255,255,0)
        time.sleep(0.05)
        dotstar[0] = (0,0,0)
        time.sleep(0.05)
        times += 1

def dotstar_mqtt_disconnect():
    dotstar[0] = (0,0,0)
    times = 0
    while times < 5:
        dotstar[0] = (0,255,255)
        time.sleep(0.05)
        dotstar[0] = (0,0,0)
        time.sleep(0.05)
        times += 1

def dotstar_sitting():
    dotstar[0] = (0,0,0)
    times = 0
    while times < 3:
        dotstar[0] = (255,255,0)
        time.sleep(1.00)
        dotstar[0] = (0,0,0)
        time.sleep(1.00)
        times += 1

try:
    from secrets import secrets
except ImportError:
    dotstar_error()

try:
  wifi.radio.connect(secrets["ssid"], secrets["password"])
except ValueError as err:
    dotstar_error()    
except ConnectionError as err:
    dotstar_error()


times = 0
dotstar_wifi_success()

### Feeds ###
sitting_feed = "sitting_time/sitting"

# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    dotstar_mqtt_success()

def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    dotstar_mqtt_disconnect()

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=secrets["broker"],
    port=secrets["port"],
    username=secrets["aio_username"],
    password=secrets["aio_key"],
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected

mqtt_client.connect()

# blue, right front
touch1 = touchio.TouchIn(board.A10)
# green, left front
touch2 = touchio.TouchIn(board.A5)
# yellow, left back
touch3 = touchio.TouchIn(board.A2)
# red, right back
touch4 = touchio.TouchIn(board.A6)

# Poll the message queue
mqtt_client.loop()

if touch1.value or touch2.value or touch3.value or touch4.value:
    mqtt_client.publish(sitting_feed, 1)
    dotstar_sitting()
else:
    mqtt_client.publish(sitting_feed, 0)

sleep_time = 120
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + sleep_time)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
