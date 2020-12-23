import os
import json
import paho.mqtt.subscribe as sub
import paho.mqtt.publish as publish
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime


# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
engine = create_engine("mysql://root@localhost/sbs")
db = scoped_session(sessionmaker(bind=engine))


key1 = 1
key2 = 0
temp_threshold = 0

def check(a):
    global key1
    global key2
    if a == 1:
        key1 -= 1
        if key1 <= 0:
            key1 = 9
            return True
    else:
        key2 -= 1
        if key2 < 0:
            key2 = 5
            return True
    return False

def print_msg_1(client, userdata, message):
    global temp_threshold
    # print(message.payload)
    data = str(message.payload.decode())
    # print(type(data))
    data = json.loads(data)
    # print(type(data))
    light_threshold = db.execute("SELECT temp_threshold FROM room WHERE room_id="+data["room"]).fetchone()[0]
    if int(data["value"]) > light_threshold:
        devices = db.execute("SELECT device_id FROM device WHERE type = 'air' AND room_id="+data["room"])
        for device in devices:
            device_control(device["device_id"])
        print(f"""Temp: {data["value"]}""")
        try:
            # db.execute("INSERT INTO light (device_id, light_intensity, time) VALUES (:device_id, :light, :time)",
            #            {"device_id": 2, "light": data["value"], "time": t.strftime('%Y-%m-%d %H:%M:%S')})
            db.execute("UPDATE device SET status=1 WHERE type='air' AND room_id="+ data["room"])
            db.commit()
        finally:
            db.close()
        print("Done")

def device_control(device_id):
    p_data = {}
    p_data["device_id"] = device_id
    p_data["value"] = 1
    data = json.dumps(p_data)
    publish.single("Topic/Temp", data, hostname="broker.hivemq.com")
    # publish.single("Topic/LightD", data, hostname="13.76.250.158", auth={'username': "BKvm2", 'password': "Hcmut_CSE_2020"})


sub.callback(print_msg_1, "TempSensor", hostname ="broker.hivemq.com")
# sub.callback(print_msg, "Topic/Light", hostname="13.76.250.158", auth={'username':"BKvm2", 'password':"Hcmut_CSE_2020"})
# mosquitto_pub -h broker.hivemq.com -p 1883 -t "TempSensor" -m "{\"room\":\"1\", \"value\":30}"