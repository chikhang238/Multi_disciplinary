import paho.mqtt.publish as publish
import json
import random

while (True):
    light_data = {}
    light_data["room"] = random.randint(1, 4)
    light_data["value"] = random.randint(150, 500)
    light_data = json.dumps(light_data)
    publish.single("LightSensor", light_data, hostname="broker.hivemq.com")

    temp_data = {}
    temp_data["room"] = random.randint(1, 4)
    temp_data["value"] = random.randint(15, 50)
    temp_data = json.dumps(temp_data)
    publish.single("TempSensor", temp_data, hostname="broker.hivemq.com")