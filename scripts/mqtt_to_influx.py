import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone

# InfluxDB settings
INFLUX_URL = "http://localhost:9999"
INFLUX_TOKEN = "GsXPu7wZjThLPe9S3tLzLDrc4ioJIlOWpsi9deQL4KxRruUSw9NdhdCaD8-1iUPkJ6WmZEcpp71FrIpib4m3Yg=="
INFLUX_ORG = "Team3"
INFLUX_BUCKET = "Factory"

# MQTT settings
MQTT_BROKER = "10.10.20.10"
MQTT_PORT = 1883

# Connect to InfluxDB
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def on_message(client, userdata, msg):
    topic = msg.topic
    value = msg.payload.decode()
    field = topic.split("/")[-1]

    try:
        value = float(value)
    except:
        value = 1.0 if value.lower() == "true" else 0.0

    point = Point("factory_data") \
        .tag("source", "PLC-SIM01") \
        .field(field, value) \
        .time(datetime.now(timezone.utc))

    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
    print(f"Stored: {field} = {value}")

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.subscribe("factory/#")

print("Listening to MQTT and storing to InfluxDB...")
mqtt_client.loop_forever()
