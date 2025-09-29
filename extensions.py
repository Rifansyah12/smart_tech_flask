import pymysql
import paho.mqtt.client as mqtt
import threading
from flask import make_response

# ------------------------
# Database
# ------------------------
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="smart_nose",
        cursorclass=pymysql.cursors.DictCursor
    )

# ------------------------
# MQTT Config
# ------------------------
BROKER = "smartnose-uninus.cloud.shiftr.io"
PORT = 1883
USERNAME = "smartnose-uninus"
PASSWORD = "0DKItrqWCc9bbr5w"
TOPIC = "smartnose-uninus/#"

# Mapping topic → sensor
TOPIC_MAP = {
    "smartnose-uninus/data/mq3": "sensor1",
    "smartnose-uninus/data/mq4": "sensor2",
    "smartnose-uninus/data/mq5": "sensor3",
    "smartnose-uninus/data/mq6": "sensor4",
    "smartnose-uninus/data/mq7": "sensor5",
    "smartnose-uninus/data/mq8": "sensor6",
    # "smartnose-uninus/data/mq135": "sensor7", 
    # "smartnose-uninus/data/mq131": "sensor8",
    # "smartnose-uninus/data/mq137": "sensor9",
    # "smartnose-uninus/data/TGS822": "sensor10",    # kalau mau ditampilkan juga
}

# Menyimpan nilai sensor terakhir
sensor_state = {v: None for v in TOPIC_MAP.values()}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT Connected")
        client.subscribe(TOPIC, qos=1)

def on_message(client, userdata, msg):
    try:
        payload = int(msg.payload.decode())  # ubah ke int
        topic = msg.topic
        if topic in TOPIC_MAP:
            sensor_name = TOPIC_MAP[topic]
            sensor_state[sensor_name] = payload
            print(f"📩 {sensor_name} ({topic}): {payload}")
        else:
            print(f"ℹ️ Topic {topic} tidak dipetakan")
    except Exception as e:
        print("❌ MQTT Error:", e)

client = mqtt.Client(client_id="vsmqtt_client_5d7e")
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

def mqtt_loop():
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

threading.Thread(target=mqtt_loop, daemon=True).start()

# ------------------------
# No Cache
# ------------------------
def nocache(view):
    def no_cache(*args, **kwargs):
        resp = make_response(view(*args, **kwargs))
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '-1'
        return resp
    no_cache.__name__ = view.__name__
    return no_cache
